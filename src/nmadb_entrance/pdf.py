#!/usr/bin/python
# -*- coding: utf-8 -*-


""" PDF generators.
"""


import os
import datetime

import reportlab
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.lib import units, styles as pdf_styles, pagesizes, colors
from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        )

from project import settings
from nmadb_entrance.config import info
from nmadb_entrance import models


reportlab.rl_config.warnOnMissingFontGlyphs = 0
# Register fonts:
for font_type in ('R', 'B', 'I', 'BI'):
    font_name = 'Ubuntu-' + font_type
    path = os.path.join(settings.STATIC_ROOT, 'fonts', font_name + '.ttf')
    pdfmetrics.registerFont(ttfonts.TTFont(font_name, path))


def get_styles():
    """ Returns PDF StyleSheet.
    """

    styles = pdf_styles.getSampleStyleSheet()

    enums = reportlab.lib.enums

    styles.add(pdf_styles.ParagraphStyle(name='Heading'))
    styles['Heading'].alignment = enums.TA_CENTER
    styles['Heading'].fontSize = 13
    styles['Heading'].fontName = 'Ubuntu-B'

    styles.add(pdf_styles.ParagraphStyle(name='SubHeading'))
    styles['SubHeading'].alignment = enums.TA_JUSTIFY
    styles['SubHeading'].fontSize = 11
    styles['SubHeading'].fontName = 'Ubuntu-B'

    styles.add(pdf_styles.ParagraphStyle(name='Note'))
    styles['Note'].alignment = enums.TA_JUSTIFY
    styles['Note'].fontSize = 11
    styles['Note'].fontName = 'Ubuntu-I'

    styles.add(pdf_styles.ParagraphStyle(name='TableCellLeft'))
    styles['TableCellLeft'].alignment = enums.TA_LEFT
    styles['TableCellLeft'].fontSize = 11
    styles['TableCellLeft'].fontName = 'Ubuntu-R'

    styles.add(pdf_styles.ParagraphStyle(name='TableCellCenter'))
    styles['TableCellCenter'].alignment = enums.TA_CENTER
    styles['TableCellCenter'].fontSize = 11
    styles['TableCellCenter'].fontName = 'Ubuntu-R'

    styles['Normal'].alignment = enums.TA_JUSTIFY
    styles['Normal'].fontSize = 11
    styles['Normal'].fontName = 'Ubuntu-R'
    #styles['Normal'].firstLineIndent = 0.5*units.cm

    styles.add(pdf_styles.ParagraphStyle(name='TableAligned'))
    styles['TableAligned'].alignment = enums.TA_JUSTIFY
    styles['TableAligned'].fontSize = 11
    styles['TableAligned'].fontName = 'Ubuntu-R'
    styles['TableAligned'].leftIndent = 0.7 * units.cm

    styles.add(pdf_styles.ParagraphStyle(name='TableAlignedNote'))
    styles['TableAlignedNote'].alignment = enums.TA_JUSTIFY
    styles['TableAlignedNote'].fontSize = 11
    styles['TableAlignedNote'].fontName = 'Ubuntu-I'
    styles['TableAlignedNote'].leftIndent = 0.7 * units.cm

    styles.add(pdf_styles.ParagraphStyle(name='TableIn'))
    styles['TableIn'].alignment = enums.TA_JUSTIFY
    styles['TableIn'].fontSize = 11
    styles['TableIn'].fontName = 'Ubuntu-R'
    styles['TableIn'].leading = 0.7 * units.cm

    return styles


def get_table_styles():
    """ Returns dict fo table styles.
    """

    styles = {}

    styles['Normal'] = TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Ubuntu-R'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])

    styles['Pupil'] = TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Ubuntu-R'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])

    return styles


def render_content(file_type, content, base_info):
    """ From content creates pdf file and saves it to database.
    """

    pdf_file = models.PDFFile()
    pdf_file.base_info = base_info
    pdf_file.file_type = file_type
    pdf_file.save()

    doc = SimpleDocTemplate(
            pdf_file.global_path(),
            pagesize=pagesizes.A4,
            leftMargin=1.5*units.cm,
            rightMargin=1.5*units.cm,
            topMargin=1.5*units.cm,
            )

    def footer(canvas, doc):
        """ Adds footer.
        """

        canvas.drawString(
                1 * units.cm,
                1 * units.cm,
                ('Registracijos identifikatorius: {0.id}:{0.uuid} {1}'
                    ).format(
                    base_info,
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    doc.build(content, footer, footer)


def get_teacher_form_header(base_info, teacher_info=None):
    """ Creates the header of teacher form.
    """

    styles = get_styles()
    table_styles = get_table_styles()

    content = []

    content.append(Paragraph(
        u'Mokytojo rekomendacija<br />Nacionalinei moksleivių akademijai',
        styles['Heading']))

    content.append(Spacer(1, 0.5*units.cm))

    content.append(Paragraph((u'''
Pasirašytą rekomendaciją prašome atsiųsti kartu su mokinio
prašymu Nacionalinei moksleivių akademijai paprastu
paštu adresu {0.address},
<font name="Ubuntu-BI">iki {0.forms_send_deadline}</font>
(spaudo data).
        ''').format(info),
                             styles['Note']))

    content.append(Spacer(1, 0.5*units.cm))

    content.append(Paragraph((u'''
Rekomenduojamas mokinys:
<font name="Ubuntu-B">{0.first_name} {0.last_name}</font>'''
                              ).format(base_info), styles['Normal']))

    content.append(Spacer(1, 0.5*units.cm))

    content.append(Paragraph((u'''
Informacija apie rekomendaciją parašiusį asmenį:'''
                              ).format(base_info), styles['SubHeading']))

    content.append(Spacer(1, 0.5*units.cm))

    def getter(*attributes):
        if teacher_info is None:
            return u''
        else:
            return u' '.join([
                unicode(getattr(teacher_info, attribute))
                for attribute in attributes])

    teacher_data = [
            [u'Vardas, pavardė:', getter('first_name', 'last_name')],
            [u'Adresas kontaktams:', getter('address')],
            [u'Kontaktinis telefonas:', getter('phone_number')],
            [u'El. pašto adresas (BŪTINAS!):', getter('email')],
            [u'Mokykla:', base_info.school.title],
            [(
                u'Išsilavinimas, kvalifikacinė kategorija, mokslo, '
                u'pedagoginiai vardai:'),
                getter('qualification')],
            ]
    if teacher_info is None:
        teacher_data.extend([
            [u'Esate mokinio:', u''],
            [(
                u'&nbsp;&nbsp;&nbsp;&nbsp;Klasės vadovas(-ė) / '
                u'auklėtoja(s):'), u''],
            [(
                u'&nbsp;&nbsp;&nbsp;&nbsp;Dalyko '
                u'<font name="Ubuntu-I">(įrašykite, kokio)</font> '
                u'mokytojas:'), u''],
            [(
                u'&nbsp;&nbsp;&nbsp;&nbsp;Kita '
                u'<font name="Ubuntu-I">(įrašykite)</font>:'), u''],
            ])
    else:
        relationships = []
        if teacher_info.class_master:
            relationships.append(u'klasės auklėtojas')
        if teacher_info.subject_teacher:
            relationships.append(
                    teacher_info.subject_teacher + u' mokytojas')
            # TODO: Sutvarkyti linksnius.
        if teacher_info.other_relation:
            relationships.append(teacher_info.other_relation)
        teacher_data.append([
            u'Esate mokinio',
            u'<br />'.join(relationships)
            ])

    teacher_data.append(
            [u'Kiek metų pažįstate mokinį(-ę)?', getter('years')])
    if teacher_info is None:
        teacher_data.append([
            u'Ar mokinio(-ės) šeima yra socialiai remtina? (pabraukti)',
            u'Taip / Ne'])
    else:
        teacher_data.append([
            u'Ar mokinio(-ės) šeima yra socialiai remtina?',
            u'Taip' if teacher_info.social else u'Ne'])

    teacher_info = Table(
        [
            [
                Paragraph(cell, styles['TableCellLeft'])
                if isinstance(cell, unicode) else cell
                for cell in row
                ]
            for row in teacher_data
            ],
        colWidths=(6.5 * units.cm, 11 * units.cm),
        )
    teacher_info.setStyle(table_styles['Normal'])
    content.append(teacher_info)

    return content


def generate_teacher_hand_form(base_info):
    """ Generates teacher form for filling by hand.
    """

    styles = get_styles()
    table_styles = get_table_styles()

    content = get_teacher_form_header(base_info)

    content.append(Spacer(1, 0.5*units.cm))

    content.append(Paragraph((u'''
Prašome įvertinti mokinį(-ę) pagal šiuos kriterijus
(pažymėkite atitinkamą langelį <font name="Ubuntu-B">X</font>):'''
                              ).format(base_info), styles['Normal']))

    content.append(Spacer(1, 0.5*units.cm))

    p = lambda x: Paragraph(x, styles['TableCellCenter'])
    evaluations = [
            u'Puikiai', u'Labai gerai', u'Gerai',
            u'Pakan-<br />kamai', u'Silpnai',
            u'Nebuvo galimybės įvertinti',
            ]
    evallen = len(evaluations)
    abilities = Table([
        [u''] + [p(evaluation) for evaluation in evaluations],
        [p(u'Sisteminio mąstymo gebėjimai')] + [u''] * evallen,
        [p(u'Analitinio mąstymo gebėjimai')] + [u''] * evallen,
        [p(u'Dedukcinio mąstymo gebėjimai')] + [u''] * evallen,
        [p(u'Mokinio gebėjimas mokytis savarankiškai')] + [u''] * evallen,
        [p(u'Mokinio gebėjimas dirbti komandoje')] + [u''] * evallen,
        [p(u'Gebėjimas reikšti mintis žodžiu')] + [u''] * evallen,
        [p(u'Gebėjimas reikšti mintis raštu')] + [u''] * evallen,
        [p(u'Mokinio imlumas mokslui (mokslumas)')] + [u''] * evallen,
        ],
        colWidths=[4.5 * units.cm] + [2.2 * units.cm] * evallen)
    abilities.setStyle(table_styles['Normal'])
    content.append(abilities)

    content.append(Spacer(1, 0.5*units.cm))

    content.append(Paragraph((
        u'''
Žemiau prašome pateikti komentarus ar pastebėjimus apie {0}
pasiekimus, kurie, Jūsų manymu, galėtų turėti įtakos vertinant
{1} galimybes mokytis Nacionalinės moksleivių akademijos
sekcijoje <font name="Ubuntu-I">{2}</font>:'''
        ).format(
            u'mokinio' if base_info.gender == u'M' else u'mokinės',
            u'jo' if base_info.gender == u'M' else u'jos',
            base_info.section.title,
            ),
        styles['Normal']))

    content.append(Spacer(1, 5*units.cm))

    content.append(Table([[
        Paragraph(u'Data:', styles["Normal"]),
        Paragraph(u'Parašas:', styles["Normal"])]]))

    render_content(u'TH', content, base_info)


def generate_pupil_filled_form(base_info, pupil_info):
    """ Generates pupil form from his answers.
    """

    styles = get_styles()
    table_styles = get_table_styles()

    content = []

    p = lambda x: Paragraph(x, styles['Normal'])

    children_data_table_1 = Table(
            [
                [
                    p(u'Mokinys:'),
                    p(u' '.join([
                        base_info.first_name, base_info.last_name]))],
                [
                    p(u'El. pašto adresas:'),
                    p(base_info.email),
                    ]
                ],
            colWidths=(5 * units.cm, 8 * units.cm)
            )
    children_data_table_1.setStyle(table_styles['Pupil'])

    header_text_table = Table([
        [Paragraph((u'''
Prašymas priimti mokytis<br /> Nacionalinei moksleivių akademijai
            '''),
            styles['Heading'])],
        [Paragraph((u'''
Anketą reikia užpildyti ir būtinai atsiųsti spausdintą variantą
<font name="Ubuntu-B">su parašu</font> Nacionalinei moksleivių
akademijai paprastu paštu adresu {0.address},
<font name="Ubuntu-B">iki {0.forms_send_deadline}</font>
(spaudo data).
            ''').format(info),
            styles['Note'])],
        [children_data_table_1],
        ])
    header_table = Table(
            [[
                header_text_table,
                Paragraph(u'Vieta nuotraukai', styles['TableCellCenter']),
                ]],
            colWidths=(14.5 * units.cm, 3 * units.cm),
            )
    header_table.setStyle(TableStyle([
        ('BOX', (1, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (1, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ]
        ))

    content.append(header_table)

    s = lambda x: x.replace(u'\n', u'<br />')

    children_data_table_2 = Table([
        (p(u'Mokykla:'), p(base_info.school.title)),
        (p(u'Klasė:'), p(unicode(base_info.school_class))),
        (p(u'Sekcija:'), p(base_info.section.title)),
        (p(u'Namų adresas:'), p(base_info.generated_address)),
        (p(u'Telefono numeris:'), p(pupil_info.phone_number)),
        (p(u'Gimimo data:'),
            p(pupil_info.birth_date.strftime(u'%Y-%m-%d'))),
        ],
        colWidths=(5 * units.cm, 11.5 * units.cm)
        )
    children_data_table_2.setStyle(table_styles['Pupil'])
    content.append(children_data_table_2)

    participation_from = info.year - 2
    participation_to = info.year
    qa = [
            ((
                u'Dalyvavimas tarptautiniuose konkursuose {0} – {1} '
                u'metais:').format(participation_from, participation_to),
                pupil_info.international_achievements),
            ((
                u'Dalyvavimas nacionaliniuose konkursuose {0} – {1} '
                u'metais:').format(participation_from, participation_to),
                pupil_info.national_achievements),
            ((
                u'Dalyvavimas rajono / miesto konkursuose {0} – {1} '
                u'metais:').format(participation_from, participation_to),
                pupil_info.district_achievements),
            ((
                u'Apdovanojimai pasirinktos dalykinės srities veikloje:'
                ),
                pupil_info.scholarschips),
            ((
                u'Kita veikla ir pasiekimai:'),
                pupil_info.other_achievements),
            ((
                u'Interesai, domėjimosi sritys:'),
                pupil_info.interests),
            ((
                u'Motyvuokite, kodėl norite dalyvauti Akademijoje '
                u'bei dalykinėje grupėje {0}:').format(
                    base_info.section.title),
                pupil_info.motivation),
            ((
                u'Aš po dešimties metų:'),
                pupil_info.future),
            ((
                u'Iš kur sužinojai apie Nacionalinę moksleivių akademiją:'),
                pupil_info.come_from),
            ]
    for question, answer in qa:
        if answer:
            content.append(Spacer(1, 0.5*units.cm))
            content.append(Paragraph(question, styles['TableAlignedNote']))
            content.append(Spacer(1, 0.2*units.cm))
            content.append(Paragraph(s(answer), styles['TableAligned']))

    content.append(Spacer(1, 0.5*units.cm))

    content.append(Table([[
        Paragraph(u'Data:', styles["Normal"]),
        Paragraph(u'Parašas:', styles["Normal"])]],
        colWidths=(8 * units.cm, 8 * units.cm)))

    render_content('PC', content, base_info)


def generate_director_form(base_info, director_info=None):
    """ Generates director form for filling by hand.
    """

    styles = get_styles()
    table_styles = get_table_styles()

    content = []

    content.append(Paragraph(
        u'Mokyklos vadovo rekomendacija<br />Nacionalinei moksleivių '
        u'akademijai',
        styles['Heading']))

    content.append(Spacer(1, 0.5*units.cm))

    content.append(Paragraph((u'''
Pasirašytą rekomendaciją prašome atsiųsti kartu su mokinio
prašymu Nacionalinei moksleivių akademijai paprastu
paštu adresu {0.address},
<font name="Ubuntu-BI">iki {0.forms_send_deadline}</font>
(spaudo data).''').format(info),
                             styles['Note']))

    content.append(Spacer(1, 0.5*units.cm))

    content.append(Paragraph((u'''
Rekomenduojamas mokinys:
<font name="Ubuntu-B">{0.first_name} {0.last_name}</font>'''
                              ).format(base_info), styles['Normal']))

    content.append(Spacer(1, 0.5*units.cm))

    content.append(Paragraph((u'''
Informacija apie rekomendaciją parašiusį asmenį:'''
                              ).format(base_info), styles['SubHeading']))

    content.append(Spacer(1, 0.5*units.cm))

    def getter(*attributes):
        if director_info is None:
            return u''
        else:
            return u' '.join([
                unicode(getattr(director_info, attribute))
                for attribute in attributes])

    director_data = [
            [u'Vardas, pavardė:', getter('first_name', 'last_name')],
            [u'Adresas kontaktams:', getter('address')],
            [u'Kontaktinis telefonas:', getter('phone_number')],
            [u'El. pašto adresas:', getter('email')],
            [u'Mokykla:', base_info.school.title],
            [u'Kiek metų mokinys(-ė) mokosi šioje mokykloje?',
                getter('study_years')],
            ]
    if director_info is None:
        director_data.append([
            u'Ar mokinio(-ės) šeima yra socialiai remtina? (pabraukti)',
            u'Taip / Ne'])
    else:
        director_data.append([
            u'Ar mokinio(-ės) šeima yra socialiai remtina?',
            u'Taip' if director_info.social else u'Ne'])

    director_info_table = Table(
        [
            [
                Paragraph(cell, styles['TableCellLeft'])
                if isinstance(cell, unicode) else cell
                for cell in row
                ]
            for row in director_data
            ],
        colWidths=(6.5 * units.cm, 11 * units.cm),
        )
    director_info_table.setStyle(table_styles['Normal'])
    content.append(director_info_table)

    content.append(Spacer(1, 0.5*units.cm))

    content.append(Paragraph((u'''
<font name="Ubuntu-B">Prie rekomendacijos prašome pridėti išrašą
su mokinio(-ės) {1}/{2} mokslo metų metiniais įvertinimais.</font>
''').format(
            base_info, info.year - 1, info.year),
            styles['Normal']))

    content.append(Spacer(1, 0.5*units.cm))

    content.append(Paragraph((
        u'''
Žemiau prašome pateikti komentarus ar pastebėjimus apie {0}
pasiekimus, kurie, Jūsų manymu, galėtų turėti įtakos vertinant
{1} galimybes mokytis Nacionalinės moksleivių akademijos
sekcijoje <font name="Ubuntu-I">{2}</font>:'''
        ).format(
            u'mokinio' if base_info.gender == u'M' else u'mokinės',
            u'jo' if base_info.gender == u'M' else u'jos',
            base_info.section.title,
            ),
        styles['Normal']))

    content.append(Spacer(1, 0.5*units.cm))

    if director_info is None:
        content.append(Spacer(1, 4*units.cm))
    else:
        content.append(Paragraph(
            director_info.comment.replace(u'\n', u'<br />'),
            styles['Normal']))

    content.append(Spacer(1, 0.5*units.cm))

    content.append(Table([[
        Paragraph(u'Data:', styles["Normal"]),
        Paragraph(u'Parašas:', styles["Normal"])]]))

    if director_info is None:
        render_content(u'DH', content, base_info)
    else:
        render_content(u'DC', content, base_info)


def generate_teacher_filled_form(base_info, teacher_info):
    """ Generates teacher form from his answers.
    """

    styles = get_styles()
    table_styles = get_table_styles()

    content = get_teacher_form_header(base_info, teacher_info)

    content.append(Spacer(1, 0.5*units.cm))

    content.append(Paragraph(
        u'Prašome įvertinti mokinį(-ę) pagal šiuos kriterijus:',
        styles['Normal']))

    content.append(Spacer(1, 0.5*units.cm))

    abilities = Table([
        [
            Paragraph(
                teacher_info._meta.get_field(field).verbose_name + u':',
                styles['Normal']),
            Paragraph(
                getattr(teacher_info, 'get_' + field + '_display')(),
                styles['Normal']),]
        for field in u'''
        systemic_thinking_ability analytical_thinking_ability
        deductive_thinking_ability self_studying_ability
        team_working_ability oral_expression_ability
        written_expression_ability receptivity_ability
        '''.split()
        ])
    abilities.setStyle(table_styles['Normal'])
    content.append(abilities)

    content.append(Spacer(1, 0.5*units.cm))

    content.append(Paragraph((
        u'''
Žemiau prašome pateikti komentarus ar pastebėjimus apie {0}
pasiekimus, kurie, Jūsų manymu, galėtų turėti įtakos vertinant
{1} galimybes mokytis Nacionalinės moksleivių akademijos
sekcijoje <font name="Ubuntu-I">{2}</font>:'''
        ).format(
            u'mokinio' if base_info.gender == u'M' else u'mokinės',
            u'jo' if base_info.gender == u'M' else u'jos',
            base_info.section.title,
            ),
        styles['Normal']))

    content.append(Paragraph(
        teacher_info.comment.replace(u'\n', u'<br />'),
        styles['Normal']))

    content.append(Spacer(1, 1*units.cm))

    content.append(Table([[
        Paragraph(u'Data:', styles["Normal"]),
        Paragraph(u'Parašas:', styles["Normal"])]]))

    render_content(u'TC', content, base_info)
