import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def generate_docx(output_path=r"C:\Users\bbone\Downloads\crime_project\Indian_Crime_Prediction_Report.docx"):
    doc = docx.Document()
    
    # Page setup
    section = doc.sections[0]
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)
    section.different_first_page_header_footer = True
    
    # Base styling
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(6)
    normal_style.paragraph_format.space_before = Pt(0)
    
    # Footer page numbers for subsequent pages
    footer = section.footer
    p_ft = footer.paragraphs[0]
    p_ft.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_ft = p_ft.add_run()
    run_ft.font.name = 'Times New Roman'
    run_ft.font.size = Pt(11)
    
    fld1 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="begin"/>')
    instr = parse_xml(f'<w:instrText {nsdecls("w")} xml:space="preserve"> PAGE </w:instrText>')
    fld2 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="separate"/>')
    fld3 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="end"/>')
    run_ft._r.append(fld1)
    run_ft._r.append(instr)
    run_ft._r.append(fld2)
    run_ft._r.append(fld3)

    # Helper functions
    def set_cell_background(cell, fill_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

    def set_table_borders(table, color="B0B0B0", sz="4"):
        tblPr = table._tbl.tblPr
        borders = parse_xml(f'''
            <w:tblBorders {nsdecls("w")}>
                <w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:insideV w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:left w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:right w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>
            </w:tblBorders>
        ''')
        tblPr.append(borders)

    def add_p(text="", bold_prefix=None, italic_prefix=None, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=6, line_spacing=1.15):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        
        if bold_prefix:
            r_b = p.add_run(bold_prefix)
            r_b.font.name = 'Times New Roman'
            r_b.font.size = Pt(12)
            r_b.bold = True
        if italic_prefix:
            r_i = p.add_run(italic_prefix)
            r_i.font.name = 'Times New Roman'
            r_i.font.size = Pt(12)
            r_i.italic = True
        if text:
            r = p.add_run(text)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(12)
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(14)
        r.bold = True
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(11)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12.5)
        r.bold = True
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.bold = True
        r.italic = True
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.font.name = 'Times New Roman'
            rb.font.size = Pt(12)
            rb.bold = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        return p

    def add_code_block(code_str):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.5)
        set_cell_background(cell, "F2F2F2")
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:top w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
                <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
                <w:left w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
                <w:right w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
            </w:tcBorders>
        ''')
        tcPr.append(borders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(code_str)
        r.font.name = 'Consolas'
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(30, 30, 30)
        
        p_after = doc.add_paragraph()
        p_after.paragraph_format.space_before = Pt(0)
        p_after.paragraph_format.space_after = Pt(4)

    def add_custom_table(headers, data_rows, caption, col_widths=None):
        p_cap = doc.add_paragraph()
        p_cap.paragraph_format.space_before = Pt(8)
        p_cap.paragraph_format.space_after = Pt(4)
        p_cap.paragraph_format.keep_with_next = True
        rc = p_cap.add_run(caption)
        rc.font.name = 'Times New Roman'
        rc.font.size = Pt(10.5)
        rc.bold = True
        
        table = doc.add_table(rows=len(data_rows) + 1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(table, color="B0B0B0", sz="4")
        
        hdr_cells = table.rows[0].cells
        for i, title in enumerate(headers):
            hdr_cells[i].text = title
            set_cell_background(hdr_cells[i], "E6E6E6")
            p = hdr_cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            for run in p.runs:
                run.font.name = 'Times New Roman'
                run.font.size = Pt(10)
                run.bold = True
                
        for r_idx, row_data in enumerate(data_rows):
            row_cells = table.rows[r_idx + 1].cells
            bg_color = "F9F9F9" if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, val in enumerate(row_data):
                row_cells[c_idx].text = str(val)
                set_cell_background(row_cells[c_idx], bg_color)
                p = row_cells[c_idx].paragraphs[0]
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                is_num = str(val).replace('.', '', 1).replace('-', '', 1).replace('%', '', 1).isdigit()
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if is_num and c_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
                for run in p.runs:
                    run.font.name = 'Times New Roman'
                    run.font.size = Pt(9.5)
                    
        if col_widths:
            for row in table.rows:
                for idx, width in enumerate(col_widths):
                    row.cells[idx].width = Inches(width)
                    
        p_space = doc.add_paragraph()
        p_space.paragraph_format.space_before = Pt(0)
        p_space.paragraph_format.space_after = Pt(4)

    def add_image_fig(img_path, caption, width=Inches(5.5)):
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(6)
            p_img.paragraph_format.space_after = Pt(2)
            run = p_img.add_run()
            run.add_picture(img_path, width=width)
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(8)
            rc = p_cap.add_run(caption)
            rc.font.name = 'Times New Roman'
            rc.font.size = Pt(10)
            rc.bold = True

    # -------------------------------------------------------------
    # PAGE 1: COVER PAGE
    # -------------------------------------------------------------
    logo_path = r"C:\Users\bbone\Downloads\lpu-logo-lovely_professional_university.png"
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(6)
        p_logo.paragraph_format.space_after = Pt(20)
        run_logo = p_logo.add_run()
        run_logo.add_picture(logo_path, width=Inches(3.3))
        
    p_badge = doc.add_paragraph()
    p_badge.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_badge.paragraph_format.space_before = Pt(6)
    p_badge.paragraph_format.space_after = Pt(4)
    r_badge = p_badge.add_run("DATA SCIENCE")
    r_badge.font.name = 'Times New Roman'
    r_badge.font.size = Pt(13)
    r_badge.bold = True
    rPr = r_badge._r.get_or_add_rPr()
    rPr.append(parse_xml(f'<w:highlight {nsdecls("w")} w:val="yellow"/>'))

    p_proj = doc.add_paragraph()
    p_proj.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_proj.paragraph_format.space_before = Pt(2)
    p_proj.paragraph_format.space_after = Pt(2)
    r_proj = p_proj.add_run("PROJECT REPORT")
    r_proj.font.name = 'Times New Roman'
    r_proj.font.size = Pt(13)
    r_proj.bold = True

    p_sem = doc.add_paragraph()
    p_sem.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sem.paragraph_format.space_before = Pt(2)
    p_sem.paragraph_format.space_after = Pt(32)
    r_sem = p_sem.add_run("(Project Semester : 3rd year 1st semester)")
    r_sem.font.name = 'Times New Roman'
    r_sem.font.size = Pt(12)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(14)
    p_title.paragraph_format.space_after = Pt(40)
    r_title = p_title.add_run("INDIAN CRIME TREND ANALYSIS AND PREDICTION\nUSING MACHINE LEARNING")
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(15)
    r_title.bold = True

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(6)
    p_sub.paragraph_format.space_after = Pt(6)
    r_sub = p_sub.add_run("Submitted by:")
    r_sub.font.name = 'Times New Roman'
    r_sub.font.size = Pt(12)

    p_student = doc.add_paragraph()
    p_student.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_student.paragraph_format.space_before = Pt(2)
    p_student.paragraph_format.space_after = Pt(2)
    r_st_name = p_student.add_run("BONENI VARSHITH\n")
    r_st_name.font.name = 'Times New Roman'
    r_st_name.font.size = Pt(12.5)
    r_st_name.bold = True
    
    r_st_details = p_student.add_run(
        "Registration No. 12407267\n"
        "Roll No. 11\n"
        "Program and Section: Predictive Analysis and RK3P24PSA11\n\n"
        "Course Code: INT234\n\n"
        "Under the Guidance of\n\n"
        "Tanima Thakur\n\n\n"
        "Discipline of CSE/IT\n"
        "Lovely School of Computer Science and engineering\n"
        "Lovely Professional University, Phagwara"
    )
    r_st_details.font.name = 'Times New Roman'
    r_st_details.font.size = Pt(11.5)

    doc.add_page_break()

    # -------------------------------------------------------------
    # PAGE 2: DECLARATION
    # -------------------------------------------------------------
    p_dec_t = doc.add_paragraph()
    p_dec_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dec_t.paragraph_format.space_before = Pt(40)
    p_dec_t.paragraph_format.space_after = Pt(28)
    r_dec = p_dec_t.add_run("DECLARATION")
    r_dec.font.name = 'Times New Roman'
    r_dec.font.size = Pt(14)
    r_dec.bold = True

    add_p(
        "I, Boneni Varshith, student of predictive analysis under CSE/IT Discipline at, Lovely Professional "
        "University, Punjab, hereby declare that all the information furnished in this project report is based "
        "on my own intensive work and is genuine.",
        space_after=180
    )

    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(30)
    p_sig.paragraph_format.space_after = Pt(6)
    r_d = p_sig.add_run("Date: 29/10/26\t\t\t\t\t\tSignature: Varshith\n")
    r_d.font.name = 'Times New Roman'
    r_d.font.size = Pt(12)
    r_reg = p_sig.add_run("Registration No. 12407267\t\t\t\t\tBoneni Varshith")
    r_reg.font.name = 'Times New Roman'
    r_reg.font.size = Pt(12)

    doc.add_page_break()

    # -------------------------------------------------------------
    # PAGE 3: CERTIFICATE
    # -------------------------------------------------------------
    p_cert_t = doc.add_paragraph()
    p_cert_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert_t.paragraph_format.space_before = Pt(40)
    p_cert_t.paragraph_format.space_after = Pt(28)
    r_cert = p_cert_t.add_run("CERTIFICATE")
    r_cert.font.name = 'Times New Roman'
    r_cert.font.size = Pt(14)
    r_cert.bold = True

    add_p(
        'This is to certify that Boneni Varshith bearing Registration no. 12407267 has completed INT234 '
        'project titled, "Indian Crime Trend Analysis and Prediction Using Machine Learning" under my '
        'guidance and supervision. To the best of my knowledge, the present work is the result of the '
        'student\'s original development, effort and study.',
        space_after=150
    )

    p_guide = doc.add_paragraph()
    p_guide.paragraph_format.space_before = Pt(20)
    p_guide.paragraph_format.space_after = Pt(6)
    r_g = p_guide.add_run(
        "Signature: ___________________________\n"
        "Tanima Thakur\n"
        "School of Computer Science and Engineering\n"
        "Lovely Professional University\n"
        "Phagwara, Punjab.\n\n"
        "Date: 29/10/26 ."
    )
    r_g.font.name = 'Times New Roman'
    r_g.font.size = Pt(12)

    doc.add_page_break()

    # -------------------------------------------------------------
    # PAGE 4: ACKNOWLEDGEMENT
    # -------------------------------------------------------------
    p_ack_t = doc.add_paragraph()
    p_ack_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ack_t.paragraph_format.space_before = Pt(36)
    p_ack_t.paragraph_format.space_after = Pt(24)
    r_ack = p_ack_t.add_run("ACKNOWLEDGEMENT")
    r_ack.font.name = 'Times New Roman'
    r_ack.font.size = Pt(14)
    r_ack.bold = True

    add_p(
        "I would like to express my sincere gratitude to my project guide, Tanima Thakur, for her continuous "
        "guidance, valuable suggestions and encouragement during this project. Her clear explanation of the "
        "concepts of Machine Learning, Predictive Analysis and Statistical Inference helped me to understand "
        "the complete workflow of a data-driven project, from the cleaning and validation of official government "
        "crime records to the rigorous evaluation of the predictive models."
    )
    add_p(
        "I thank Lovely Professional University and the Discipline of CSE/IT for giving me the opportunity "
        "and the state-of-the-art facilities to do this work. I am also deeply thankful to all the faculty "
        "members who taught me the foundational courses in data science, statistics and machine learning."
    )
    add_p(
        "I acknowledge the National Crime Records Bureau (NCRB), Ministry of Home Affairs, Government of "
        "India, and the Open Government Data (OGD) Platform India (data.gov.in) for compiling and publishing "
        "the annual district-level crime statistics. The open-source Python scientific computing ecosystem—including "
        "pandas, NumPy, SciPy, Matplotlib, seaborn and scikit-learn—made it possible to conduct the comprehensive "
        "statistical tests and predictive machine learning analysis presented in this report."
    )
    add_p(
        "Finally, I thank my family and my friends for their unwavering support and motivation throughout the project."
    )

    p_ack_sign = doc.add_paragraph()
    p_ack_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_ack_sign.paragraph_format.space_before = Pt(36)
    p_ack_sign.paragraph_format.space_after = Pt(6)
    r_as = p_ack_sign.add_run("Boneni Varshith\nRegistration No. 12407267")
    r_as.font.name = 'Times New Roman'
    r_as.font.size = Pt(12)
    r_as.bold = True

    doc.add_page_break()

    # -------------------------------------------------------------
    # PAGE 5: TABLE OF CONTENTS (Exact synchronized page numbers)
    # -------------------------------------------------------------
    p_toc_t = doc.add_paragraph()
    p_toc_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc_t.paragraph_format.space_before = Pt(16)
    p_toc_t.paragraph_format.space_after = Pt(12)
    r_toc = p_toc_t.add_run("TABLE OF CONTENTS")
    r_toc.font.name = 'Times New Roman'
    r_toc.font.size = Pt(13)
    r_toc.bold = True

    toc_synced_items = [
        ("1. Introduction", "7"),
        ("   1.1 Background", "7"),
        ("   1.2 Problem Statement", "7"),
        ("   1.3 Why District-Level Modeling and Inter-Crime Prediction", "8"),
        ("   1.4 Objectives of the Project", "8"),
        ("   1.5 Scope and Limitations", "8"),
        ("   1.6 Project Workflow", "9"),
        ("   1.7 Tools and Libraries Used", "9"),
        ("2. Source of Dataset", "10"),
        ("   2.1 Origin of the Dataset", "10"),
        ("   2.2 Description of the File dstrIPC_2013.csv", "10"),
        ("   2.3 Description of the Columns", "11"),
        ("   2.4 Classification of IPC Crimes", "12"),
        ("   2.5 Reason for Selecting This Dataset", "12"),
        ("   2.6 Data Use and Ethical Note", "13"),
        ("3. EDA Process", "13"),
        ("   3.1 Overview of the Steps", "13"),
        ("   3.2 Initial Inspection", "13"),
        ("   3.3 Missing Values and Anomaly Checks", "14"),
        ("   3.4 Handling the Data Cleaning", "14"),
        ("   3.5 Outliers and Value Distributions", "15"),
        ("   3.6 Creating the Target and Derived Features", "15"),
        ("   3.7 Visual Exploration", "16"),
        ("   3.8 Splitting the Data", "20"),
        ("4. Analysis on Dataset", "20"),
        ("   4.1 Correlation Analysis", "20"),
        ("   4.2 One-way ANOVA: Crime Variations Across Geographic Zones", "23"),
        ("   4.3 Two-Sample Statistical Test: Regional Crime Disparity", "24"),
        ("   4.4 Chi-square Test: Geographic Zone and High Murder Risk", "25"),
        ("   4.5 Simple Linear Regression (Burglary vs Theft)", "26"),
        ("   4.6 Multiple Linear Regression (OLS Murder Modeling)", "28"),
        ("   4.7 Polynomial Regression (Nonlinear Crime Linkages)", "30"),
        ("   4.8 Comparison of the Regression Models", "31"),
        ("   4.9 Logistic Regression (Classifying High Murder Risk)", "32"),
        ("   4.10 K-Nearest Neighbours (kNN)", "33"),
        ("   4.11 Gaussian Naive Bayes", "34"),
        ("   4.12 Decision Tree Classifier", "34"),
        ("   4.13 Support Vector Machine (SVM)", "36"),
        ("   4.14 Master Comparison of the Classification Models", "36"),
        ("5. Conclusion", "38"),
        ("   5.1 Summary of the Work", "38"),
        ("   5.2 Results of the Models", "38"),
        ("   5.3 Achievement of the Objectives", "39"),
        ("   5.4 Limitations", "39"),
        ("6. Future Scope", "39"),
        ("7. References", "40")
    ]

    for title, page_str in toc_synced_items:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.tab_stops.add_tab_stop(Inches(6.5), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        p_t.paragraph_format.space_before = Pt(0)
        p_t.paragraph_format.space_after = Pt(1.5)
        p_t.paragraph_format.line_spacing = 1.0
        
        r1 = p_t.add_run(title)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(9.5)
        if not title.startswith("   "):
            r1.bold = True
            
        p_t.add_run("\t")
        
        r3 = p_t.add_run(page_str)
        r3.font.name = 'Times New Roman'
        r3.font.size = Pt(9.5)
        if not title.startswith("   "):
            r3.bold = True

    doc.add_page_break()

    # -------------------------------------------------------------
    # PAGE 6: LIST OF FIGURES & LIST OF TABLES (Exact synchronized pages)
    # -------------------------------------------------------------
    p_lof_t = doc.add_paragraph()
    p_lof_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lof_t.paragraph_format.space_before = Pt(10)
    p_lof_t.paragraph_format.space_after = Pt(6)
    r_lof = p_lof_t.add_run("LIST OF FIGURES")
    r_lof.font.name = 'Times New Roman'
    r_lof.font.size = Pt(11.5)
    r_lof.bold = True

    lof_synced = [
        ("Figure 1: Total registered IPC crimes by category, India 2013", "17"),
        ("Figure 2: Top 10 states/UTs by total registered IPC crimes", "18"),
        ("Figure 3: Top 10 districts by total registered IPC crimes", "18"),
        ("Figure 4: Distribution of total IPC crimes per district", "19"),
        ("Figure 5: Total IPC crimes across geographic zones", "20"),
        ("Figure 6: Correlation heat map of IPC crime categories", "22"),
        ("Figure 7: Simple linear regression: Burglary vs Theft", "27"),
        ("Figure 8: Multiple linear regression: actual vs predicted murder cases", "29"),
        ("Figure 9: Polynomial regression (degree 2 curve) for burglary vs theft", "31"),
        ("Figure 10: Test RMSE comparison of regression models", "32"),
        ("Figure 11: Choosing k for the kNN classifier", "34"),
        ("Figure 12: Feature importance of the decision tree classifier", "35"),
        ("Figure 13: Decision tree structure for high murder risk", "36"),
        ("Figure 14: Confusion matrices of the five classification models", "37"),
        ("Figure 15: ROC curves of the classification models", "37"),
        ("Figure 16: F1 score comparison of the classification models", "38")
    ]

    for title, page_str in lof_synced:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.tab_stops.add_tab_stop(Inches(6.5), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        p_t.paragraph_format.space_before = Pt(0)
        p_t.paragraph_format.space_after = Pt(1)
        p_t.paragraph_format.line_spacing = 1.0
        
        r1 = p_t.add_run(title)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(8.5)
        p_t.add_run("\t")
        r3 = p_t.add_run(page_str)
        r3.font.name = 'Times New Roman'
        r3.font.size = Pt(8.5)

    p_lot_t = doc.add_paragraph()
    p_lot_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lot_t.paragraph_format.space_before = Pt(10)
    p_lot_t.paragraph_format.space_after = Pt(6)
    r_lot = p_lot_t.add_run("LIST OF TABLES")
    r_lot.font.name = 'Times New Roman'
    r_lot.font.size = Pt(11.5)
    r_lot.bold = True

    lot_synced = [
        ("Table 1: Tools and libraries used in the project", "9"),
        ("Table 2: Summary of the raw file dstrIPC_2013.csv", "10"),
        ("Table 3: Primary columns and descriptions of the dataset", "11"),
        ("Table 4: Major IPC crime classifications and penal provisions", "12"),
        ("Table 5: Data cleaning and administrative unit filtering summary", "14"),
        ("Table 6: Summary of the cleaned crime dataset", "16"),
        ("Table 7: Partition of data for regression and classification modeling", "20"),
        ("Table 8: Pearson correlation of IPC crime categories with Murder and Theft", "21"),
        ("Table 9: Zone-wise summary of total IPC crimes and murder cases", "23"),
        ("Table 10: Contingency table: Geographic zone and high murder risk (Chi-square test)", "25"),
        ("Table 11: Simple linear regression compared with baseline (Theft prediction)", "26"),
        ("Table 12: Coefficients of the multiple linear regression model (OLS)", "28"),
        ("Table 13: Polynomial regression evaluation across degrees 1 to 5", "30"),
        ("Table 14: Summary performance of the regression models on test data", "31"),
        ("Table 15: Master performance comparison of the classification models", "36"),
        ("Table 16: Objectives of the project and the results achieved", "39")
    ]

    for title, page_str in lot_synced:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.tab_stops.add_tab_stop(Inches(6.5), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        p_t.paragraph_format.space_before = Pt(0)
        p_t.paragraph_format.space_after = Pt(1)
        p_t.paragraph_format.line_spacing = 1.0
        
        r1 = p_t.add_run(title)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(8.5)
        p_t.add_run("\t")
        r3 = p_t.add_run(page_str)
        r3.font.name = 'Times New Roman'
        r3.font.size = Pt(8.5)

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 1: INTRODUCTION (STARTS ON PAGE 7)
    # -------------------------------------------------------------
    add_h1("1. Introduction")
    
    add_h2("1.1 Background")
    add_p(
        "Crime prevention, public safety and judicial administration represent paramount societal challenges "
        "in modern India. With a population exceeding 1.2 billion people distributed across 35 States and Union "
        "Territories, law enforcement agencies face complex operational challenges in allocating personnel, "
        "monitoring criminal hot spots, and preventing severe violent outbreaks. Under the Indian Penal Code "
        "(IPC), offenses span a broad spectrum ranging from severe violent crimes against persons (such as murder, "
        "attempt to murder, rape, and kidnapping) to property offenses (such as burglary, dacoity, and theft) and "
        "crimes against public order (including riots and arson)."
    )
    add_p(
        "To provide empirical transparency and institutional accountability, the National Crime Records Bureau "
        "(NCRB) under the Ministry of Home Affairs, Government of India, collects annual district-level crime data "
        "from thousands of police stations across the country. In the past, crime statistics were reviewed primarily "
        "as historical tables or post-hoc annual audits. However, the advancement of modern Data Science and "
        "Machine Learning provides an unprecedented opportunity to analyze multivariate criminal dependencies, "
        "identify structural anomalies across administrative districts, and construct predictive decision models "
        "that can empower proactive policing, strategic resource allocation, and targeted administrative interventions."
    )

    add_h2("1.2 Problem Statement")
    add_p(
        "Most conventional law enforcement analyses operate retrospectively: police administrators review crime "
        "statistics only after incidents have accumulated at year-end. A police superintendent, district magistrate, "
        "or homeland security policymaker would benefit substantially more from quantitative predictive tools that "
        "characterize district vulnerability, forecast specific offense volumes from leading crime indicators, and "
        "flag districts at high risk of extreme violent outcomes. The core problems solved in this project are therefore:"
    )
    add_p(
        "Using district-level IPC crime records across India, formulate, evaluate, and compare: "
        "(a) regression models to predict specific offense volumes (forecasting theft from burglary, and estimating "
        "murder occurrences from co-occurring violent and cognizable crime vectors), and (b) classification models "
        "to predict whether a district belongs to the high-violence / high-murder risk category.",
        bold_prefix="Core Project Formulation: "
    )
    add_p(
        "A district is designated as a high-murder risk district (high_murder = 1) when its recorded murder incidents "
        "exceed the national district median threshold (median = 34 incidents in 2013). Predicting continuous crime "
        "volumes constitutes a regression problem, while categorizing districts into high vs low risk regimes represents "
        "a binary classification problem. Both predictive paradigms are systematically modeled and compared in this "
        "project so that the full curriculum of statistical learning techniques can be rigorously demonstrated and evaluated."
    )

    add_h2("1.3 Why District-Level Modeling and Inter-Crime Prediction")
    add_p(
        "State-level aggregate statistics obscure critical local variations. Within a single state, large urban "
        "metropolises and dense industrial corridors often exhibit crime profiles completely different from rural or "
        "remote hilly jurisdictions. Conducting predictive analysis at the district level preserves operational granularity. "
        "Furthermore, criminological research demonstrates that different categories of crime do not occur in isolation: "
        "property crimes such as burglary and theft share common socioeconomic and opportunistic drivers, while violent "
        "crimes such as murder, dacoity, riots, and kidnapping frequently co-occur within stressed socio-legal environments. "
        "By modeling the mathematical relationships connecting property crimes and predicting violent offenses from broad "
        "violent crime profiles, machine learning models uncover structural dependencies that cannot be revealed by univariate "
        "statistical summaries alone."
    )

    add_h2("1.4 Objectives of the Project")
    add_p("The objectives of this project are clearly defined and quantitatively evaluated with empirical benchmarks:")
    add_bullet(
        "To collect, inspect, clean, and validate official district-level IPC crime records for 2013 from the NCRB, "
        "systematically identifying and eliminating aggregate state totals (double counting) and specialized railway/GRP/CID "
        "policing units to construct a clean dataset of 754 genuine geographic districts.",
        bold_prefix="1. Data Preprocessing and Cleaning: "
    )
    add_bullet(
        "To conduct thorough Exploratory Data Analysis (EDA) and inferential hypothesis testing, using Pearson correlation, "
        "One-way ANOVA across geographic zones, regional two-sample t-tests, and Chi-Square tests of independence.",
        bold_prefix="2. Statistical Hypothesis Testing: "
    )
    add_bullet(
        "To develop and validate regression models (Simple Linear Regression, Multiple Linear Regression with analytical "
        "OLS matrix solutions, and Polynomial Regression up to degree 5) for continuous crime volume prediction. "
        "Target: Outperform the naive mean baseline in terms of MAE, RMSE, and R².",
        bold_prefix="3. Continuous Crime Volume Forecasting: "
    )
    add_bullet(
        "To formulate, tune, and evaluate five diverse classification algorithms (Logistic Regression, K-Nearest Neighbours, "
        "Gaussian Naive Bayes, Decision Trees, and Support Vector Machines) to classify high-risk murder districts. "
        "Target: Attain classification accuracy and F1-score substantially superior to the 50.3% majority-class baseline.",
        bold_prefix="4. Risk Classification Modeling: "
    )
    add_bullet(
        "To comprehensively benchmark all models using standard diagnostic evaluation metrics: MAE, MSE, RMSE, R² for regression; "
        "and Accuracy, Log Loss, ROC-AUC, Precision, Recall, F1-Score, 5-Fold Cross Validation, and Confusion Matrices for classification.",
        bold_prefix="5. Comparative Benchmarking: "
    )

    add_h2("1.5 Scope and Limitations")
    add_p(
        "The project analyzes recorded Indian Penal Code offenses across 754 verified districts in 35 States and Union "
        "Territories for the year 2013. The input variables encompass all major cognizable IPC crime heads. Because the official "
        "NCRB dataset available for this study represents a single cross-sectional annual census (2013), longitudinal time-series "
        "forecasting across successive future years cannot be performed without multi-year records. Furthermore, crime numbers "
        "represent raw recorded counts rather than per-capita rates, as synchronized decennial census population denominators "
        "at the district level were not included in the raw table. All predictions apply strictly to district-level administrative "
        "aggregates and never to individuals."
    )

    add_h2("1.6 Project Workflow")
    add_p("The end-to-end analytical pipeline was executed in eight sequential phases:")
    add_bullet("Formulation of the societal domain challenge, identifying criminological predictive objectives.", bold_prefix="1. Problem Definition: ")
    add_bullet("Raw data acquisition, schema inspection, data type validation, and initial missing value checks.", bold_prefix="2. Data Acquisition: ")
    add_bullet("Auditing state totals (ZZ TOTAL), filtering railway/GRP units, and column renaming.", bold_prefix="3. Preprocessing: ")
    add_bullet("Univariate, bivariate, and zonal visualizations, Pearson correlations, ANOVA, and Chi-square tests.", bold_prefix="4. EDA and Statistics: ")
    add_bullet("80/20 train-test partitioning stratified by risk class, and feature standardization via StandardScaler.", bold_prefix="5. Partitioning: ")
    add_bullet("Simple, multiple, and polynomial regression modeling; OLS matrix closed-form verification.", bold_prefix="6. Regression Modeling: ")
    add_bullet("Training and hyperparameter tuning of Logistic Regression, kNN, Naive Bayes, Decision Trees, and SVM.", bold_prefix="7. Classification: ")
    add_bullet("Comprehensive benchmarking on unseen test data, ROC curves, confusion matrices, and synthesis.", bold_prefix="8. Evaluation & Review: ")

    add_h2("1.7 Tools and Libraries Used")
    add_p(
        "The entire computational workflow was implemented in Python 3. The open-source libraries utilized and their "
        "functional roles are detailed in Table 1."
    )

    t1_headers = ["Tool / Library", "Version Scope", "Functional Purpose in Project"]
    t1_rows = [
        ["Python 3.14 / 3.x", "Core Runtime", "Primary programming environment for scientific computing and modeling"],
        ["pandas", "Data Structures", "Dataframe ingestion, cleaning, aggregation, grouping, and CSV serialization"],
        ["NumPy", "Linear Algebra", "Vectorized array calculations, matrix algebra, and closed-form OLS derivation"],
        ["SciPy (stats)", "Inferential Stats", "Pearson correlation tests, one-way ANOVA, two-sample t-tests, Chi-square"],
        ["Matplotlib", "Data Visualization", "Plotting histograms, scatter plots, horizontal bar charts, and ROC curves"],
        ["seaborn", "Statistical Viz", "Generating correlation heatmaps, multi-panel box plots, and confusion matrices"],
        ["scikit-learn", "Machine Learning", "Regression, classification, feature scaling, model tuning, and metrics"]
    ]
    add_custom_table(t1_headers, t1_rows, "Table 1: Tools and libraries used in the project", [1.6, 1.4, 3.5])

    # -------------------------------------------------------------
    # CHAPTER 2: SOURCE OF DATASET
    # -------------------------------------------------------------
    add_h1("2. Source of Dataset")

    add_h2("2.1 Origin of the Dataset")
    add_p(
        "The primary dataset used in this study is the official district-level Indian Penal Code crime repository, "
        "compiled and verified by the National Crime Records Bureau (NCRB), Ministry of Home Affairs, Government of India. "
        "The NCRB serves as the apex national agency responsible for collecting, consolidating, and analyzing crime intelligence "
        "from state police headquarters and union territory administrations. The specific dataset, titled 'Crime in India 2013 "
        "- District-wise IPC Crimes', is publicly disseminated on the Open Government Data Platform India (data.gov.in) "
        "to facilitate empirical research, public policy evaluation, and academic data science inquiry."
    )

    add_h2("2.2 Description of the File dstrIPC_2013.csv")
    add_p(
        "The raw input file is titled dstrIPC_2013.csv. Each row in the file records the annual incident counts across "
        "30 distinct IPC offense classifications for a given police jurisdiction or administrative district within a State or "
        "Union Territory during calendar year 2013. Table 2 provides a quantitative structural summary of the raw data file "
        "prior to any cleaning or filtering operations."
    )

    t2_headers = ["Item / Structural Attribute", "Observed Value", "Remarks and Characteristics"]
    t2_rows = [
        ["Total Raw Rows", "823", "Encompasses districts, railway police units, and aggregate totals"],
        ["Total Columns", "33", "2 text identifiers, 1 year column, 30 numerical crime counts"],
        ["Number of States / UTs", "35", "Covers all 28 states and 7 union territories (2013 boundaries)"],
        ["Calendar Year Covered", "2013", "Single-year comprehensive national crime census"],
        ["Level of Aggregation", "District / Unit", "Annual cumulative recorded cases per policing jurisdiction"],
        ["Identified Aggregate Rows", "35 rows ('ZZ TOTAL')", "Summary rows representing statewide sums (must be filtered)"],
        ["Identified Non-District Units", "34 rows (Railway/GRP/CID)", "Specialized policing units operating across district lines"],
        ["Duplicate Rows", "0", "No exact duplicate records present in raw file"],
        ["Missing / Null Cells", "0", "Zero missing values; unrecorded incidents are entered as 0"]
    ]
    add_custom_table(t2_headers, t2_rows, "Table 2: Summary of the raw file dstrIPC_2013.csv", [2.0, 1.4, 3.1])

    add_h2("2.3 Description of the Columns")
    add_p(
        "The dataset contains 33 columns. The first three columns specify the administrative hierarchy (State/UT, "
        "District name, and Year), while the remaining 30 columns quantify specific cognizable crime categories codified "
        "under the Indian Penal Code. The definitions, penal provisions, and data types of key columns are summarized in Table 3."
    )

    t3_headers = ["Column Identifier", "IPC Penal Section", "Criminological Definition / Offense Scope", "Data Type"]
    t3_rows = [
        ["state_ut", "Administrative", "Name of the State or Union Territory", "Text"],
        ["district", "Administrative", "Name of the revenue district or policing unit", "Text"],
        ["year", "Temporal", "Calendar year of data collection (2013)", "Integer"],
        ["murder", "Section 302 IPC", "Offense of culpable homicide amounting to murder", "Integer"],
        ["attempt_to_murder", "Section 307 IPC", "Acts committed with intention or knowledge to cause death", "Integer"],
        ["culpable_homicide", "Section 304 IPC", "Culpable homicide not amounting to murder", "Integer"],
        ["rape", "Section 376 IPC", "Sexual assault offenses codified under IPC", "Integer"],
        ["kidnapping_abduction", "Section 363-369 IPC", "Unlawful removal or abduction of persons from guardianship", "Integer"],
        ["dacoity", "Section 395 IPC", "Aggravated robbery committed by five or more persons conjointly", "Integer"],
        ["robbery", "Section 392 IPC", "Theft or extortion involving violence or threat of violence", "Integer"],
        ["burglary", "Section 442-460 IPC", "Lurking house-trespass or house-breaking to commit offenses", "Integer"],
        ["theft", "Section 378 IPC", "Dishonest taking of movable property out of possession", "Integer"],
        ["riots", "Section 146-148 IPC", "Use of force or violence by an unlawful assembly", "Integer"],
        ["criminal_breach_of_trust", "Section 405 IPC", "Dishonest misappropriation of property entrusted", "Integer"],
        ["cheating", "Section 415-420 IPC", "Fraudulent inducement causing wrongful loss or damage", "Integer"],
        ["arson", "Section 435-438 IPC", "Mischief by fire or explosive substance with intent to destroy", "Integer"],
        ["hurt_grevious_hurt", "Section 319-338 IPC", "Voluntarily causing hurt or grievous bodily injuries", "Integer"],
        ["dowry_deaths", "Section 304B IPC", "Homicidal or unnatural deaths connected to dowry demands", "Integer"],
        ["cruelty_by_husband", "Section 498A IPC", "Cruelty or harassment of women by husband or in-laws", "Integer"],
        ["causing_death_negligence", "Section 304A IPC", "Fatal accidents or deaths caused by rash or negligent acts", "Integer"],
        ["total_ipc_crimes", "Aggregate Index", "Cumulative total of all cognizable IPC offenses registered", "Integer"]
    ]
    add_custom_table(t3_headers, t3_rows, "Table 3: Primary columns and descriptions of the dataset", [1.6, 1.4, 2.7, 0.8])

    add_h2("2.4 Classification of IPC Crimes")
    add_p(
        "In Indian jurisprudence and criminological analysis, IPC offenses are categorized into broad functional classes "
        "reflecting the nature of the harm inflicted. Table 4 categorizes these offenses."
    )

    t4_headers = ["Broad Crime Category", "Representative Offenses Included", "Societal & Law Enforcement Impact"]
    t4_rows = [
        ["Violent Crimes Against Person", "Murder, Attempt to Murder, Culpable Homicide, Rape, Kidnapping", "Severe threat to life and human security; primary focus of high-level policing"],
        ["Crimes Against Property", "Dacoity, Robbery, Burglary, Theft", "Direct economic harm to citizens; indicative of street security and patrol adequacy"],
        ["Crimes Against Women", "Rape, Dowry Deaths, Cruelty by Husband/Relatives, Molestation", "Critical indicator of gender safety and social justice enforcement"],
        ["Public Order Offenses", "Rioting, Unlawful Assembly, Arson", "Threatens community cohesion, communal harmony, and civic peace"],
        ["Economic & White-Collar", "Cheating, Criminal Breach of Trust, Counterfeiting", "Erodes institutional trust and business integrity across commercial centers"],
        ["Negligent Fatalities", "Causing Death by Negligence (Traffic accidents, industrial lapses)", "Highlights transportation safety, regulatory compliance, and civic infrastructure"]
    ]
    add_custom_table(t4_headers, t4_rows, "Table 4: Major IPC crime classifications and penal provisions", [1.8, 2.2, 2.5])

    add_h2("2.5 Reason for Selecting This Dataset")
    add_p("The selection of the NCRB district crime dataset is grounded in four major factors:")
    add_bullet(
        "Critical Societal Impact: Public safety, crime reduction, and judicial resource planning represent pressing national "
        "priorities directly affecting the welfare of millions of Indian citizens.",
        bold_prefix="1. Societal Importance: "
    )
    add_bullet(
        "Dual Analytical Modeling Paradigms: The presence of both continuous crime counts and categorical risk thresholds enables "
        "the simultaneous formulation of regression and classification machine learning architectures.",
        bold_prefix="2. Methodological Versatility: "
    )
    add_bullet(
        "Data Authenticity and Real-World Nuance: Official administrative records contain genuine structural complexities "
        "(such as administrative total rows and non-geographic units) requiring rigorous, justified data cleaning.",
        bold_prefix="3. Authentic Complexity: "
    )
    add_bullet(
        "Geographic Granularity: The dataset encompasses 754 verified districts across 35 States/UTs, providing sufficient "
        "sample size for robust statistical hypothesis testing, train-test splitting, and 5-fold cross-validation.",
        bold_prefix="4. Statistical Power: "
    )

    add_h2("2.6 Data Use and Ethical Note")
    add_p(
        "The data utilized in this study consists solely of anonymized, aggregated administrative crime counts at the district "
        "level published under the Open Government Data License India. It contains zero personally identifiable information (PII), "
        "individual victim records, or offender identities. The findings and predictive models developed herein are intended solely "
        "for academic research and machine learning pedagogy. Model outputs represent district-level administrative risk indicators "
        "and must never be interpreted as individual risk assessments or behavioral profiling."
    )

    # -------------------------------------------------------------
    # CHAPTER 3: EDA PROCESS
    # -------------------------------------------------------------
    add_h1("3. EDA Process")

    add_h2("3.1 Overview of the Steps")
    add_p(
        "Exploratory Data Analysis (EDA) is the foundational stage wherein raw data is systematically inspected, verified, "
        "cleaned, transformed, and explored before building machine learning models. In this project, EDA followed six rigorous steps: "
        "(i) initial structural inspection of schema and data types; (ii) verification of missing values and negative anomalies; "
        "(iii) mathematical verification and removal of statewide double-counting totals (ZZ TOTAL); (iv) identification and filtering "
        "of specialized non-district policing units (railway, GRP, CID); (v) construction of target labels and derived features; and "
        "(vi) visual exploration through univariate distributions, bivariate correlations, and zonal boxplots."
    )

    add_h2("3.2 Initial Inspection")
    add_p(
        "The raw file dstrIPC_2013.csv was loaded using pandas. Initial inspection revealed exactly 823 rows and 33 columns. "
        "The state and district text fields were inspected for trailing whitespaces. Numerical columns were checked for invalid negative "
        "values. Zero negative counts were discovered. Furthermore, a comprehensive scan for null or NaN values revealed exactly zero "
        "missing cells across all 823 rows, confirming that unrecorded crime occurrences were explicitly entered as 0 by the NCRB."
    )

    add_p("Python Code (Program 1: loading and inspecting raw data)", bold_prefix="")
    code_p1 = (
        'import pandas as pd\n'
        '\n'
        '# Load raw dataset\n'
        'crime = pd.read_csv("data/raw/dstrIPC_2013.csv")\n'
        '\n'
        '# Inspect dimensions and schema\n'
        'print("Shape:", crime.shape)\n'
        'print("Columns:", list(crime.columns))\n'
        'print("Data types summary:\\n", crime.dtypes.value_counts())\n'
        '\n'
        '# Verify missing values, duplicates, and negative counts\n'
        'print("Total missing values:", crime.isnull().sum().sum())\n'
        'print("Duplicate rows:", crime.duplicated().sum())\n'
        'print("Negative values:", (crime.iloc[:, 3:] < 0).sum().sum())\n'
        'print("States/UTs count:", crime["STATE/UT"].nunique())\n'
        'print("Districts count:", crime["DISTRICT"].nunique())\n'
    )
    add_code_block(code_p1)

    add_h2("3.3 Missing Values and Anomaly Checks")
    add_p(
        "Although standard automated functions like df.isnull().sum() reported zero missing entries, substantive domain inspection "
        "revealed severe structural anomalies that would completely invalidate machine learning models if uncorrected. Specifically, "
        "the raw file contained two distinct classes of invalid rows: (1) statewide summary aggregate rows labeled 'ZZ TOTAL', and "
        "(2) specialized policing units that do not represent geographic revenue districts."
    )

    add_h2("3.4 Handling the Data Cleaning")
    add_p(
        "The data cleaning pipeline addressed these anomalies through strict, justifiable mathematical rules:",
        bold_prefix="Cleaning Strategy: "
    )
    add_bullet(
        "Elimination of Double-Counting (ZZ TOTAL): Exactly 35 rows carried the district label 'ZZ TOTAL'. An automated verification "
        "script confirmed that for all 35 States/UTs, the value in 'ZZ TOTAL' was exactly equal to the mathematical sum of all other "
        "districts within that state. Retaining these rows would double-count every single crime in the country and distort all "
        "distributions. All 35 'ZZ TOTAL' rows were safely removed.",
        bold_prefix="1. Removal of State Totals: "
    )
    add_bullet(
        "Filtering Specialized Non-District Policing Units: Thirty-four (34) rows represented specialized law enforcement units, "
        "including Government Railway Police (e.g., GUNTAKAL RLY., SECUNDERABAD RLY., PATNA RLY.), CID branches, and special crime "
        "squads. These units operate across multiple municipal districts and track jurisdiction-specific railway offenses rather than "
        "resident civilian populations. Retaining them creates false outliers with zero domestic crimes and localized transit crimes. "
        "All 34 specialized non-district units were identified via regex (RLY|RAILWAY|GRP|CID|CRIME) and eliminated.",
        bold_prefix="2. Railway and Specialized Units: "
    )
    add_bullet(
        "Standardizing Column Nomenclature: All 33 column headers were standardized to lowercase snake_case, replacing slashes, spaces, "
        "and ampersands (e.g., 'STATE/UT' -> 'state_ut', 'TOTAL IPC CRIMES' -> 'total_ipc_crimes').",
        bold_prefix="3. Header Normalization: "
    )
    add_p(
        "Following these cleaning operations, the final verified dataset comprises exactly 754 genuine geographic districts across "
        "all 35 States/UTs of India, with zero missing values and zero duplicates. Table 5 details the cleaning audit."
    )

    t5_headers = ["Preprocessing Operation", "Initial Count", "Rows Removed", "Remaining Count", "Justification & Impact"]
    t5_rows = [
        ["Raw File Ingestion", "823", "0", "823", "Initial raw dataset from NCRB / data.gov.in"],
        ["Removal of 'ZZ TOTAL' Rows", "823", "35", "788", "Eliminated exact statewide sums to prevent 100% double-counting"],
        ["Filtering Railway/GRP Units", "788", "34", "754", "Removed transit/railway policing units that are not territorial districts"],
        ["Column Name Normalization", "754", "0", "754", "Converted to lowercase snake_case for robust Python attribute access"],
        ["Null & Duplicate Audit", "754", "0", "754", "Verified 0 missing cells, 0 duplicates, and 0 negative values"]
    ]
    add_custom_table(t5_headers, t5_rows, "Table 5: Data cleaning and administrative unit filtering summary", [1.8, 1.0, 1.0, 1.1, 2.6])

    add_p("Python Code (Program 2: data cleaning and preparation)", bold_prefix="")
    code_p2 = (
        'import pandas as pd\n'
        '\n'
        'crime = pd.read_csv("data/raw/dstrIPC_2013.csv")\n'
        'crime["STATE/UT"] = crime["STATE/UT"].str.strip()\n'
        'crime["DISTRICT"] = crime["DISTRICT"].str.strip().str.upper()\n'
        '\n'
        '# Remove ZZ TOTAL aggregate rows (35 states)\n'
        'crime = crime[crime["DISTRICT"] != "ZZ TOTAL"]\n'
        '\n'
        '# Remove railway police and specialized CID/crime-branch units (34 units)\n'
        'special = crime["DISTRICT"].str.contains(r"RLY|RAILWAY|GRP|CID|CRIME", regex=True)\n'
        'crime = crime[~special]\n'
        '\n'
        '# Standardize column headers to clean snake_case\n'
        'crime.columns = [c.strip().lower().replace("/", "_").replace(" ", "_").replace("&", "and") for c in crime.columns]\n'
        '\n'
        '# Save pristine cleaned dataset\n'
        'crime.to_csv("data/cleaned_crime_data.csv", index=False)\n'
        'print("Cleaned dataset shape:", crime.shape)  # exactly (754, 33)\n'
    )
    add_code_block(code_p2)

    add_h2("3.5 Outliers and Value Distributions")
    add_p(
        "Inspection of the numerical distributions across the 754 districts revealed intense right-skewness. In major metropolitan "
        "centers such as Delhi, Mumbai, Bengaluru, and Patna, total registered crimes exceed 15,000 cases annually, whereas small "
        "rural districts in the North-East and island territories record fewer than 100 cases. For instance, the maximum district total "
        "is 33,262 crimes, while the median is 2,494.5 crimes and the mean is 3,519.4 crimes. Because tree-based models and non-parametric "
        "classifiers are invariant to monotonic scale transformations, raw counts were retained, while standard scaling was applied "
        "for distance-based and gradient-sensitive models (kNN, Logistic Regression, SVM)."
    )

    add_h2("3.6 Creating the Target and Derived Features")
    add_p("To support both regression and classification machine learning architectures, two target structures were defined:")
    add_bullet(
        "Regression Targets: Predicting district theft cases from burglary counts (modeling property crimes), and predicting district "
        "murder cases from leading violent crime indicators (attempt to murder, robbery, dacoity, riots, arson, hurt, kidnapping).",
        bold_prefix="1. Continuous Targets: "
    )
    add_bullet(
        "Classification Target (high_murder): A binary indicator variable designating whether a district experiences high murder risk. "
        "The national median for district murder counts is exactly 34 cases. Districts with murder > 34 were assigned high_murder = 1 "
        "(375 districts, 49.7%), while districts with murder <= 34 were assigned high_murder = 0 (379 districts, 50.3%). This yields "
        "a balanced, objective target free from arbitrary class imbalance.",
        bold_prefix="2. Binary Risk Target: "
    )
    add_bullet(
        "Geographic Zone Mapping: To enable inferential statistical hypothesis testing (One-way ANOVA and Chi-Square tests), all 35 "
        "States and Union Territories were categorized into six standard geographic zones: North (196 districts), East (129 districts), "
        "South (126 districts), West (121 districts), North-East (104 districts), and Central (78 districts).",
        bold_prefix="3. Geographic Zones: "
    )
    add_p("Table 6 provides comprehensive summary statistics of the final cleaned dataset across all 754 districts.")

    t6_headers = ["Statistical Metric", "Total IPC Crimes", "Murder Cases", "Theft Cases", "Burglary Cases"]
    t6_rows = [
        ["Total Recorded Cases (National)", "2,653,607", "33,201", "380,483", "107,750"],
        ["Mean Count per District", "3,519.4", "44.0", "504.6", "142.9"],
        ["Median Count per District", "2,494.5", "34.0", "283.0", "87.5"],
        ["Standard Deviation", "3,591.8", "39.8", "771.2", "168.4"],
        ["Minimum Count", "1", "0", "0", "0"],
        ["25th Percentile (Q1)", "1,142.0", "15.0", "118.0", "34.0"],
        ["75th Percentile (Q3)", "4,746.5", "62.0", "598.0", "190.5"],
        ["Maximum Count", "33,262", "299", "9,890", "1,556"],
        ["High Risk Districts (Above Median)", "N/A", "375 (49.7%)", "375 (49.7%)", "374 (49.6%)"]
    ]
    add_custom_table(t6_headers, t6_rows, "Table 6: Summary of the cleaned crime dataset (754 districts)", [2.2, 1.4, 1.4, 1.4, 1.4])

    add_h2("3.7 Visual Exploration")
    add_p(
        "Exploratory graphical analysis was conducted using Matplotlib and seaborn to uncover empirical distributions, "
        "regional variations, and inter-crime correlations across the 754 districts."
    )

    add_h3("3.7.1 Crime Count by Major Category")
    add_p(
        "Figure 1 displays the total registered cases across India for the 18 primary non-overlapping IPC categories in 2013. "
        "Theft (380,483 cases) and Hurt / Grievous Hurt (347,700 cases) represent the most frequent offenses in India, followed by "
        "Cruelty by Husband or Relatives (Section 498A IPC, 118,866 cases) and Burglary (107,750 cases). Causing Death by Negligence "
        "(104,260 cases) highlights the severe impact of vehicular and industrial fatalities. Severe violent crimes such as Murder "
        "(33,201 cases) and Rape (33,707 cases) account for a smaller proportion of total volume but carry catastrophic societal harm."
    )
    add_image_fig(r"C:\Users\bbone\Downloads\crime_project\crime_project\outputs\figures\1_crime_by_category.png", "Figure 1: Total registered IPC crimes by category, India 2013")

    add_h3("3.7.2 Top 10 States/UTs by Total Registered IPC Crimes")
    add_p(
        "Figure 2 illustrates the top 10 States/UTs ranked by aggregate registered IPC crimes in 2013. Madhya Pradesh leads the nation "
        "with 272,854 recorded offenses, closely followed by Maharashtra (226,170 cases), Tamil Nadu (207,643 cases), Uttar Pradesh "
        "(203,714 cases), and Andhra Pradesh (196,444 cases). It is vital to note that these values represent unadjusted gross counts; "
        "high counts reflect large population sizes and proactive police registration policies rather than solely high criminality."
    )
    add_image_fig(r"C:\Users\bbone\Downloads\crime_project\crime_project\outputs\figures\2_top_states.png", "Figure 2: Top 10 states/UTs by total registered IPC crimes")

    add_h3("3.7.3 Top 10 Districts by Total Registered IPC Crimes")
    add_p(
        "Figure 3 reveals the 10 highest-volume districts in India. Large municipal jurisdictions dominate the list, led by Patna "
        "(Bihar) with 33,262 registered offenses, South West Delhi (27,046 cases), Bengaluru Urban (Karnataka, 26,454 cases), "
        "and Indore (Madhya Pradesh, 23,267 cases). Major administrative centers concentrate dense commercial activity and reporting "
        "infrastructure, generating substantially higher absolute crime registrations."
    )
    add_image_fig(r"C:\Users\bbone\Downloads\crime_project\crime_project\outputs\figures\3_top_districts.png", "Figure 3: Top 10 districts by total registered IPC crimes")

    add_h3("3.7.4 Distribution of Total IPC Crimes per District")
    add_p(
        "Figure 4 plots the frequency histogram of total IPC crimes per district across all 754 districts. The distribution exhibits "
        "pronounced positive skewness (right-tail). The vast majority of districts (over 65%) record between 500 and 3,500 crimes per "
        "year, while a long, sparse upper tail extends beyond 20,000 cases for major metropolitan capitals."
    )
    add_image_fig(r"C:\Users\bbone\Downloads\crime_project\crime_project\outputs\figures\4_distribution_total.png", "Figure 4: Distribution of total IPC crimes per district")

    add_h3("3.7.5 Total IPC Crimes Across Geographic Zones")
    add_p(
        "Figure 5 displays the distribution of total IPC crimes partitioned across the six geographic zones. Districts in the Southern "
        "zone (mean 5,833.3, median 4,835.0) and Western zone (mean 4,853.3, median 3,996.0) exhibit substantially higher average crime "
        "registrations than districts in the North-East zone (mean 1,022.8, median 241.0). The statistical validity of these zonal "
        "differences is formally evaluated via One-way ANOVA in Section 4.2."
    )
    add_image_fig(r"C:\Users\bbone\Downloads\crime_project\crime_project\outputs\figures\fig_box_zones.png", "Figure 5: Total IPC crimes across geographic zones")

    add_h2("3.8 Splitting the Data")
    add_p(
        "To rigorously benchmark all predictive regression and classification models without data leakage or optimistic evaluation "
        "bias, the 754 districts were partitioned into independent Training (80%) and Test (20%) datasets. For classification models, "
        "the split was stratified on the binary target high_murder to ensure that the 49.7% / 50.3% class ratio was exactly preserved "
        "across both splits. A fixed random seed (random_state=42) was utilized to ensure complete reproducibility. Table 7 details "
        "the partitioning scheme."
    )

    t7_headers = ["Partition Name", "Sampling Share", "District Count", "High Murder (Class 1)", "Low Murder (Class 0)", "Analytical Role"]
    t7_rows = [
        ["Training Set", "80.0%", "603", "300 (49.8%)", "303 (50.2%)", "Model parameter estimation, OLS fitting, cross-validation"],
        ["Test Set", "20.0%", "151", "75 (49.7%)", "76 (50.3%)", "Unseen final evaluation, generalization error benchmarking"],
        ["Full Cleaned Data", "100.0%", "754", "375 (49.7%)", "379 (50.3%)", "Total empirical population analyzed"]
    ]
    add_custom_table(t7_headers, t7_rows, "Table 7: Partition of data for regression and classification modeling", [1.6, 1.1, 1.1, 1.4, 1.4, 2.0])

    # -------------------------------------------------------------
    # CHAPTER 4: ANALYSIS ON DATASET
    # -------------------------------------------------------------
    add_h1("4. Analysis on Dataset")
    add_p(
        "This chapter is organized into two rigorous sections. Sections 4.1 through 4.4 execute inferential statistical "
        "hypothesis testing on the cleaned crime data (Pearson correlation analysis, One-way ANOVA across zones, two-sample t-testing, "
        "and Chi-Square testing of independence). Sections 4.5 through 4.14 build, tune, validate, and compare predictive models: "
        "three regression architectures (Simple Linear Regression, Multiple OLS Regression, and Polynomial Regression) and five "
        "classification architectures (Logistic Regression, kNN, Naive Bayes, Decision Trees, and Support Vector Machines). "
        "In accordance with academic report guidelines, every analysis adheres to a five-part structure: (i) Introduction, "
        "(ii) General Description, (iii) Specific Requirements, Functions and Formulas, (iv) Analysis Results, and (v) Visualization. "
        "A significance threshold of α = 0.05 (p < 0.05) is maintained for all inferential tests."
    )

    # 4.1 Correlation Analysis
    add_h2("4.1 Correlation Analysis")
    add_h3("(i) Introduction")
    add_p(
        "Correlation analysis quantifies the strength and direction of linear co-movement between pairs of continuous crime variables. "
        "Before building regression equations or classification models, it is essential to determine which crime categories co-vary "
        "with murder and theft, and to identify collinearity among input predictors."
    )
    add_h3("(ii) General Description")
    add_p(
        "The Pearson correlation coefficient (r) ranges between -1.0 and +1.0. An r value approaching +1.0 indicates strong positive "
        "linear co-movement, r = 0 indicates no linear association, and r approaching -1.0 indicates inverse co-movement. The two-tailed "
        "p-value evaluates the null hypothesis (H₀: ρ = 0) against the alternative hypothesis (H₁: ρ ≠ 0)."
    )
    add_h3("(iii) Specific Requirements, Functions and Formulas")
    add_p(
        "The analysis utilized pandas.DataFrame.corr() for the bivariate correlation matrix, scipy.stats.pearsonr() for formal p-value "
        "testing, and seaborn.heatmap() for graphical display. The mathematical formulation is:"
    )
    add_p(
        "r = Σ (xᵢ − x̄)(yᵢ − ȳ) / √[ Σ (xᵢ − x̄)² × Σ (yᵢ − ȳ)² ]",
        bold_prefix="Pearson Correlation Formula: "
    )
    add_p("where xᵢ and yᵢ represent the recorded incident counts of two crime categories in district i, with means x̄ and ȳ.")
    add_h3("(iv) Analysis Results")
    add_p(
        "Table 8 summarizes the empirical Pearson correlations of all major crime categories with Murder and Theft. Attempt to Murder "
        "(r = 0.778, p < 0.0001), Riots (r = 0.589, p < 0.0001), and Kidnapping and Abduction (r = 0.574, p < 0.0001) exhibit the "
        "strongest correlation with Murder, confirming that homicidal violence is closely intertwined with general interpersonal and "
        "organized violence. In property crime, Burglary demonstrates an exceptional correlation with Theft (r = 0.884, p < 0.0001), "
        "providing powerful justification for simple and polynomial regression modeling."
    )

    t8_headers = ["Crime Category", "r with Murder", "Murder p-value", "r with Theft", "Theft p-value"]
    t8_rows = [
        ["Burglary", "0.472", "< 0.0001", "0.884", "< 0.0001"],
        ["Attempt to Murder", "0.778", "< 0.0001", "0.468", "< 0.0001"],
        ["Riots", "0.589", "< 0.0001", "0.412", "< 0.0001"],
        ["Kidnapping & Abduction", "0.574", "< 0.0001", "0.621", "< 0.0001"],
        ["Hurt / Grievous Hurt", "0.548", "< 0.0001", "0.589", "< 0.0001"],
        ["Robbery", "0.521", "< 0.0001", "0.714", "< 0.0001"],
        ["Dacoity", "0.512", "< 0.0001", "0.384", "< 0.0001"],
        ["Rape", "0.504", "< 0.0001", "0.562", "< 0.0001"],
        ["Arson", "0.435", "< 0.0001", "0.312", "< 0.0001"],
        ["Cheating", "0.386", "< 0.0001", "0.684", "< 0.0001"]
    ]
    add_custom_table(t8_headers, t8_rows, "Table 8: Pearson correlation of IPC crime categories with Murder and Theft", [2.2, 1.2, 1.3, 1.2, 1.3])

    add_p("Python Code (Program 3: Correlation heatmap & tests)", bold_prefix="")
    code_p3 = (
        'import pandas as pd\n'
        'import seaborn as sns\n'
        'import matplotlib.pyplot as plt\n'
        'from scipy import stats\n'
        '\n'
        'crime = pd.read_csv("data/cleaned_crime_data.csv")\n'
        'main = ["murder", "attempt_to_murder", "rape", "kidnapping_and_abduction", "dacoity",\n'
        '        "robbery", "burglary", "theft", "riots", "cheating", "arson", "hurt_grevious_hurt"]\n'
        '\n'
        'corr = crime[main].corr()\n'
        'plt.figure(figsize=(10, 8))\n'
        'sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0)\n'
        'plt.title("Correlation Heatmap of Primary IPC Crime Categories (2013)")\n'
        'plt.savefig("outputs/figures/5_correlation_heatmap.png")\n'
        'plt.close()\n'
        '\n'
        'r, p = stats.pearsonr(crime["burglary"], crime["theft"])\n'
        'print(f"Burglary vs Theft: r = {r:.4f}, p = {p:.4e}")\n'
    )
    add_code_block(code_p3)

    add_h3("(v) Visualization")
    add_p("Figure 6 illustrates the complete correlation heatmap across all primary IPC crime categories.")
    add_image_fig(r"C:\Users\bbone\Downloads\crime_project\crime_project\outputs\figures\5_correlation_heatmap.png", "Figure 6: Correlation heat map of IPC crime categories")

    # 4.2 One-way ANOVA
    add_h2("4.2 One-way ANOVA: Crime Variations Across Geographic Zones")
    add_h3("(i) Introduction")
    add_p(
        "Geographic variation in crime registration across India is substantial. To rigorously evaluate whether crime volumes "
        "differ significantly across administrative zones rather than by random sampling fluctuation, a One-way Analysis of Variance "
        "(ANOVA) was conducted across the six defined geographic zones."
    )
    add_h3("(ii) General Description")
    add_p(
        "One-way ANOVA tests the null hypothesis (H₀: μ₁ = μ₂ = ... = μ₆) that the true mean crime volume is identical across all "
        "six zones against the alternative hypothesis (H₁: at least one zone exhibits a statistically different mean). The F-statistic "
        "compares the between-group mean square against the within-group mean square."
    )
    add_h3("(iii) Specific Requirements, Functions and Formulas")
    add_p("The analysis utilized scipy.stats.f_oneway(). The mathematical test statistic is:")
    add_p(
        "F = [ SSB / (k − 1) ] / [ SSW / (N − k) ]",
        bold_prefix="One-way ANOVA F-statistic: "
    )
    add_p("where k = 6 zones, N = 754 districts, between-group df₁ = k - 1 = 5, and within-group df₂ = 754 - 6 = 748.")
    add_h3("(iv) Analysis Results")
    add_p(
        "For Total IPC Crimes, the ANOVA test yielded F = 29.38 with p = 2.77 × 10⁻²⁷. For Murder, the test yielded F = 22.61 "
        "with p = 3.65 × 10⁻²¹. In both cases, p < 0.0001, decisively rejecting the null hypothesis. Geographic zone has a massive, "
        "statistically significant effect on recorded crime. As summarized in Table 9, Southern districts record the highest average "
        "total crimes (mean = 5,833.3), whereas Eastern districts record the highest average murder cases (mean = 67.6)."
    )

    t9_headers = ["Geographic Zone", "Districts", "Mean Total Crimes", "Median Total", "Mean Murder", "Median Murder"]
    t9_rows = [
        ["South", "126", "5,833.3", "4,835.0", "50.8", "42.5"],
        ["West", "121", "4,853.3", "3,996.0", "43.1", "36.0"],
        ["Central", "78", "3,597.8", "2,642.5", "39.1", "37.0"],
        ["East", "129", "3,519.4", "2,494.0", "67.6", "55.0"],
        ["North", "196", "2,377.9", "1,710.5", "39.3", "29.5"],
        ["North-East", "104", "1,022.8", "241.0", "18.7", "9.5"]
    ]
    add_custom_table(t9_headers, t9_rows, "Table 9: Zone-wise summary of total IPC crimes and murder cases", [1.8, 1.0, 1.5, 1.4, 1.3, 1.3])

    add_p("Python Code (Program 4: One-way ANOVA across zones)", bold_prefix="")
    code_p4 = (
        'from scipy import stats\n'
        '\n'
        '# Group total crimes and murder by zone\n'
        'groups_total = [g["total_ipc_crimes"].values for _, g in crime.groupby("zone")]\n'
        'f_tot, p_tot = stats.f_oneway(*groups_total)\n'
        'print(f"ANOVA Total Crimes: F = {f_tot:.2f}, p = {p_tot:.4e}")\n'
        '\n'
        'groups_murder = [g["murder"].values for _, g in crime.groupby("zone")]\n'
        'f_murd, p_murd = stats.f_oneway(*groups_murder)\n'
        'print(f"ANOVA Murder: F = {f_murd:.2f}, p = {p_murd:.4e}")\n'
    )
    add_code_block(code_p4)

    add_h3("(v) Visualization")
    add_p("Figure 5 in Chapter 3 illustrates the comparative box plot of total IPC crimes across the six geographic zones.")

    # 4.3 Two-Sample Statistical Test
    add_h2("4.3 Two-Sample Statistical Test: Regional Crime Disparity")
    add_h3("(i) Introduction")
    add_p(
        "A prominent question in Indian administrative criminology is whether northern and southern districts exhibit fundamentally "
        "divergent crime registration patterns. To test this specific hypothesis, Welch's two-sample independent t-test was conducted."
    )
    add_h3("(ii) General Description")
    add_p(
        "Welch's t-test compares the means of two independent samples with unequal variances. The null hypothesis (H₀: μ_North = μ_South) "
        "posits that northern and southern districts have equal average crime volumes, while H₁ posits a significant difference."
    )
    add_h3("(iii) Specific Requirements, Functions and Formulas")
    add_p("The function scipy.stats.ttest_ind(equal_var=False) was used. The test statistic formula is:")
    add_p(
        "t = (x̄₁ − x̄₂) / √[ (s₁² / n₁) + (s₂² / n₂) ]",
        bold_prefix="Welch's Two-Sample t-statistic: "
    )
    add_p("where n_North = 196, x̄_North = 2,377.9, s_North = 2,389.5; and n_South = 126, x̄_South = 5,833.3, s_South = 4,552.4.")
    add_h3("(iv) Analysis Results")
    add_p(
        "The test yielded t = -7.85 with p = 4.40 × 10⁻¹³. Because p < 0.0001, H₀ is emphatically rejected. Southern districts exhibit "
        "an average crime volume nearly 2.5 times higher than northern districts. This disparity is largely attributable to higher "
        "rates of FIR registration, greater police density, and higher reporting propensities in southern states rather than higher actual crime."
    )
    add_p("Python Code (Program 4b: Regional two-sample t-test)", bold_prefix="")
    code_p4b = (
        'north_crimes = crime[crime["zone"] == "North"]["total_ipc_crimes"]\n'
        'south_crimes = crime[crime["zone"] == "South"]["total_ipc_crimes"]\n'
        '\n'
        't_stat, p_val = stats.ttest_ind(north_crimes, south_crimes, equal_var=False)\n'
        'print(f"Welch t-test North vs South: t = {t_stat:.2f}, p = {p_val:.4e}")\n'
        'print(f"Mean North: {north_crimes.mean():.1f}, Mean South: {south_crimes.mean():.1f}")\n'
    )
    add_code_block(code_p4b)
    add_h3("(v) Visualization")
    add_p("The distribution difference is clearly visualized in the comparative zone distributions displayed in Figure 5.")

    # 4.4 Chi-square Test
    add_h2("4.4 Chi-square Test: Geographic Zone and High Murder Risk")
    add_h3("(i) Introduction")
    add_p(
        "While ANOVA evaluated continuous crime volumes, the Chi-Square test of independence evaluates the classification target: "
        "Is a district's risk of being a high-murder jurisdiction statistically dependent on its geographic zone?"
    )
    add_h3("(ii) General Description")
    add_p(
        "The Chi-square test compares observed cell counts in a contingency table against the counts expected under the null hypothesis "
        "of independence (H₀: Geographic zone and high murder risk are independent)."
    )
    add_h3("(iii) Specific Requirements, Functions and Formulas")
    add_p("Using pandas.crosstab() and scipy.stats.chi2_contingency(), the formula is:")
    add_p(
        "χ² = Σ [ (Oᵢⱼ − Eᵢⱼ)² / Eᵢⱼ ]",
        bold_prefix="Chi-Square Test Statistic: "
    )
    add_p("where degrees of freedom df = (rows − 1) × (cols − 1) = (6 − 1) × (2 − 1) = 5.")
    add_h3("(iv) Analysis Results")
    add_p(
        "The test produced χ² = 70.63 with df = 5 and p = 7.59 × 10⁻¹⁴. H₀ is decisively rejected. The proportion of high-murder "
        "districts varies drastically across zones. In the Eastern zone, an alarming 72.9% of districts (94 out of 129) are high-murder "
        "districts. Conversely, in the North-East zone, only 20.2% of districts (21 out of 104) exceed the median. Table 10 provides "
        "the complete contingency table."
    )

    t10_headers = ["Geographic Zone", "Low Murder (0)", "High Murder (1)", "Total Districts", "Share of High Murder"]
    t10_rows = [
        ["East", "35", "94", "129", "72.9%"],
        ["South", "56", "70", "126", "55.6%"],
        ["Central", "36", "42", "78", "53.8%"],
        ["West", "56", "65", "121", "53.7%"],
        ["North", "112", "84", "196", "42.9%"],
        ["North-East", "83", "21", "104", "20.2%"],
        ["National Total", "379", "375", "754", "49.7%"]
    ]
    add_custom_table(t10_headers, t10_rows, "Table 10: Contingency table: Geographic zone and high murder risk (Chi-square test)", [1.8, 1.3, 1.3, 1.3, 1.6])

    add_p("Python Code (Program 4c: Chi-Square test of independence)", bold_prefix="")
    code_p4c = (
        'table = pd.crosstab(crime["zone"], crime["high_murder"])\n'
        'chi2, p, dof, expected = stats.chi2_contingency(table)\n'
        'print("Contingency Table:\\n", table)\n'
        'print(f"Chi-square = {chi2:.2f}, df = {dof}, p-value = {p:.4e}")\n'
    )
    add_code_block(code_p4c)
    add_h3("(v) Visualization")
    add_p("Table 10 presents the empirical distribution of observed high-murder proportions across all geographic zones.")

    # 4.5 Simple Linear Regression
    add_h2("4.5 Simple Linear Regression (Burglary vs Theft)")
    add_h3("(i) Introduction")
    add_p(
        "Simple linear regression models the direct linear dependency between two continuous variables. Here, district burglary "
        "count is utilized as an explanatory predictor to estimate district theft volume."
    )
    add_h3("(ii) General Description")
    add_p(
        "The model fits a least-squares regression line minimizing the sum of squared residuals. To validate predictive utility, "
        "the model must be benchmarked against a baseline model (predicting the mean theft volume of the training data)."
    )
    add_h3("(iii) Specific Requirements, Functions and Formulas")
    add_p("Using scikit-learn's LinearRegression(), the equations and performance metrics are:")
    add_p("ŷ = β₁ x + β₀\nMAE = (1/n) Σ |yᵢ − ŷᵢ|\nRMSE = √[ (1/n) Σ (yᵢ − ŷᵢ)² ]\nR² = 1 − [ Σ (yᵢ − ŷᵢ)² / Σ (yᵢ − ȳ)² ]", bold_prefix="Formulations: ")
    add_h3("(iv) Analysis Results")
    add_p(
        "The fitted equation is: Theft = 3.5207 × Burglary − 18.0582. On the unseen test dataset (151 districts), the model attained "
        "MAE = 290.90, RMSE = 591.49, and R² = 0.3191. Compared to the naive mean baseline (MAE = 436.24, RMSE = 716.87, R² = -0.0001), "
        "simple linear regression reduces test RMSE by 17.5% and explains 31.9% of the variance in theft volume. Table 11 summarizes "
        "the comparative performance."
    )

    t11_headers = ["Model Architecture", "Test MAE", "Test MSE", "Test RMSE", "Test R²"]
    t11_rows = [
        ["Baseline (Mean of Train)", "436.24", "513,896.7", "716.87", "-0.0001"],
        ["Simple Linear Regression", "290.90", "349,864.2", "591.49", "0.3191"]
    ]
    add_custom_table(t11_headers, t11_rows, "Table 11: Simple linear regression compared with baseline (Theft prediction)", [2.4, 1.2, 1.3, 1.2, 1.2])

    add_p("Python Code (Program 5: Simple linear regression)", bold_prefix="")
    code_p5 = (
        'from sklearn.linear_model import LinearRegression\n'
        'from sklearn.model_selection import train_test_split\n'
        'from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score\n'
        '\n'
        'x = crime[["burglary"]]\n'
        'y = crime["theft"]\n'
        'x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)\n'
        '\n'
        'model = LinearRegression().fit(x_train, y_train)\n'
        'y_pred = model.predict(x_test)\n'
        '\n'
        'print("Slope:", round(model.coef_[0], 4))       # 3.5207\n'
        'print("Intercept:", round(model.intercept_, 4)) # -18.0582\n'
        'print(f"MAE: {mean_absolute_error(y_test, y_pred):.2f}, RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.2f}, R2: {r2_score(y_test, y_pred):.4f}")\n'
    )
    add_code_block(code_p5)

    add_h3("(v) Visualization")
    add_p("Figure 7 illustrates the fitted regression line against the actual test data points.")
    add_image_fig(r"C:\Users\bbone\Downloads\crime_project\crime_project\outputs\figures\6_simple_linear_regression.png", "Figure 7: Simple linear regression: Burglary vs Theft")

    # 4.6 Multiple Linear Regression
    add_h2("4.6 Multiple Linear Regression (OLS Murder Modeling)")
    add_h3("(i) Introduction")
    add_p(
        "Homicide does not occur in an institutional vacuum. Multiple linear regression leverages seven leading violent and "
        "cognizable crime predictors to model district murder counts."
    )
    add_h3("(ii) General Description")
    add_p(
        "Multiple regression estimates partial slope coefficients for each explanatory feature while holding all other inputs fixed. "
        "The model was estimated both via scikit-learn and analytically from first principles using the Ordinary Least Squares (OLS) "
        "normal equation matrix formulation."
    )
    add_h3("(iii) Specific Requirements, Functions and Formulas")
    add_p("The closed-form analytical OLS solution and model equation are:")
    add_p(
        "β = (Xᵀ X)⁻¹ Xᵀ y\nŷ = β₀ + β₁ x₁ + β₂ x₂ + ... + β₇ x₇",
        bold_prefix="OLS Matrix Equation: "
    )
    add_p("where X is the design matrix containing an intercept column of ones and the seven crime features.")
    add_h3("(iv) Analysis Results")
    add_p(
        "The analytical matrix inversion exactly matched scikit-learn coefficients to seven decimal places (np.allclose = True). "
        "On the unseen test data, the multiple regression model achieved MAE = 17.70, RMSE = 25.22, and R² = 0.6075. Dacoity (β = 0.4755), "
        "Attempt to Murder (β = 0.2151), and Kidnapping and Abduction (β = 0.0952) emerged as the strongest positive contributors to "
        "murder occurrences. Table 12 displays the complete parameter estimates."
    )

    t12_headers = ["Feature Variable (IPC Category)", "OLS Coefficient (β)", "Standard Error", "Criminological Interpretation"]
    t12_rows = [
        ["Intercept (β₀)", "12.9788", "1.624", "Expected baseline murder count for minimal violent activity"],
        ["attempt_to_murder (x₁)", "0.2151", "0.024", "Strong direct co-occurrence with fatal violent assaults"],
        ["robbery (x₂)", "0.0071", "0.016", "Marginal linear association with homicide volume"],
        ["dacoity (x₃)", "0.4755", "0.089", "Highest coefficient; lethal organized gang violence"],
        ["riots (x₄)", "0.0303", "0.012", "Communal and group clashes leading to fatal escalation"],
        ["arson (x₅)", "-0.0644", "0.045", "Slight negative conditional weighting after adjusting for riots"],
        ["hurt_grevious_hurt (x₆)", "0.0147", "0.003", "Widespread violent assaults occasionally resulting in fatalities"],
        ["kidnapping_and_abduction (x₇)", "0.0952", "0.018", "Ransom demands and abductions resulting in homicide"]
    ]
    add_custom_table(t12_headers, t12_rows, "Table 12: Coefficients of the multiple linear regression model (OLS)", [2.3, 1.4, 1.2, 2.5])

    add_p("Python Code (Program 6: Multiple regression & OLS derivation)", bold_prefix="")
    code_p6 = (
        '# Analytical OLS by hand: beta = (X.T @ X)^-1 @ X.T @ y\n'
        'X = np.column_stack([np.ones(len(xm_train)), xm_train.values])\n'
        'beta = np.linalg.inv(X.T @ X) @ X.T @ ym_train.values\n'
        '\n'
        'model = LinearRegression().fit(xm_train, ym_train)\n'
        'ym_pred = model.predict(xm_test)\n'
        'print("Scikit-learn matches OLS closed-form?", np.allclose(beta[1:], model.coef_))\n'
        'print(f"Test MAE: {mean_absolute_error(ym_test, ym_pred):.2f}, RMSE: {np.sqrt(mean_squared_error(ym_test, ym_pred)):.2f}, R2: {r2_score(ym_test, ym_pred):.4f}")\n'
    )
    add_code_block(code_p6)

    add_h3("(v) Visualization")
    add_p("Figure 8 illustrates the actual versus predicted murder counts along the 45-degree reference line.")
    add_image_fig(r"C:\Users\bbone\Downloads\crime_project\crime_project\outputs\figures\7_multiple_regression_actual_vs_predicted.png", "Figure 8: Multiple linear regression: actual vs predicted murder cases")

    # 4.7 Polynomial Regression
    add_h2("4.7 Polynomial Regression (Nonlinear Crime Linkages)")
    add_h3("(i) Introduction")
    add_p(
        "Relationships between crime categories may exhibit nonlinear tendencies. For instance, in heavily congested urban environments, "
        "theft opportunities may escalate nonlinearly relative to residential burglaries. Polynomial regression models this curvature."
    )
    add_h3("(ii) General Description")
    add_p(
        "Polynomial regression expands input feature x into higher powers [x, x², x³, ...] and applies linear regression on the expanded "
        "basis. However, higher-degree polynomials risk overfitting by memorizing idiosyncrasies in the training set."
    )
    add_h3("(iii) Specific Requirements, Functions and Formulas")
    add_p("Using PolynomialFeatures(degree=d), the degree 2 formulation is:")
    add_p(
        "ŷ = β₀ + β₁ x + β₂ x²",
        bold_prefix="Quadratic Polynomial Equation: "
    )
    add_h3("(iv) Analysis Results")
    add_p(
        "Polynomial models of degrees 1 through 5 were systematically evaluated on training and test sets. As summarized in Table 13, "
        "Degree 2 achieved the optimal test performance: MAE = 282.74, RMSE = 585.90, and R² = 0.3319. As degree increased to 4 and 5, "
        "training R² expanded unrealistically while test R² deteriorated sharply to 0.2650 and test RMSE rose to 614.55—classic empirical "
        "evidence of overfitting."
    )

    t13_headers = ["Polynomial Degree", "Train R²", "Test R²", "Test MAE", "Test RMSE", "Diagnosis"]
    t13_rows = [
        ["Degree 1 (Linear)", "0.8251", "0.3191", "290.90", "591.49", "Slight underfitting; assumes rigid linearity"],
        ["Degree 2 (Quadratic)", "0.8344", "0.3319", "282.74", "585.90", "Optimal balance; lowest test MAE and RMSE"],
        ["Degree 3 (Cubic)", "0.8351", "0.3221", "285.37", "590.20", "Marginal curvature overfitting begins"],
        ["Degree 4 (Quartic)", "0.8398", "0.2888", "297.16", "604.49", "Overfitting; test RMSE exceeds linear model"],
        ["Degree 5 (Quintic)", "0.8412", "0.2650", "308.06", "614.55", "Severe overfitting; high test generalization error"]
    ]
    add_custom_table(t13_headers, t13_rows, "Table 13: Polynomial regression evaluation across degrees 1 to 5", [1.6, 1.1, 1.1, 1.1, 1.1, 2.0])

    add_p("Python Code (Program 7: Polynomial regression across degrees)", bold_prefix="")
    code_p7 = (
        'from sklearn.preprocessing import PolynomialFeatures\n'
        '\n'
        'for degree in [1, 2, 3, 4, 5]:\n'
        '    poly = PolynomialFeatures(degree=degree)\n'
        '    x_tr_p = poly.fit_transform(x_train)\n'
        '    x_te_p = poly.transform(x_test)\n'
        '    m = LinearRegression().fit(x_tr_p, y_train)\n'
        '    print(f"Deg {degree} -> Test MAE: {mean_absolute_error(y_test, m.predict(x_te_p)):.2f}, RMSE: {np.sqrt(mean_squared_error(y_test, m.predict(x_te_p))):.2f}, R2: {r2_score(y_test, m.predict(x_te_p)):.4f}")\n'
    )
    add_code_block(code_p7)

    add_h3("(v) Visualization")
    add_p("Figure 9 illustrates the fitted quadratic curve (degree 2) against the empirical test distribution.")
    add_image_fig(r"C:\Users\bbone\Downloads\crime_project\crime_project\outputs\figures\8_polynomial_regression.png", "Figure 9: Polynomial regression (degree 2 curve) for burglary vs theft")

    # 4.8 Comparison of Regression Models
    add_h2("4.8 Comparison of the Regression Models")
    add_p(
        "All regression models were evaluated on the identical 151 test districts. Table 14 and Figure 10 synthesize the results."
    )

    t14_headers = ["Regression Model", "Target Variable", "Input Predictors", "Test MAE", "Test RMSE", "Test R²"]
    t14_rows = [
        ["Baseline (Mean)", "Theft", "None (Predicts training mean)", "436.24", "716.87", "-0.0001"],
        ["Simple Linear Regression", "Theft", "Burglary", "290.90", "591.49", "0.3191"],
        ["Polynomial (Degree 2)", "Theft", "Burglary + Burglary²", "282.74", "585.90", "0.3319"],
        ["Multiple Linear Regression", "Murder", "7 Violent Crime Categories", "17.70", "25.22", "0.6075"]
    ]
    add_custom_table(t14_headers, t14_rows, "Table 14: Summary performance of the regression models on test data", [2.0, 1.0, 2.0, 1.0, 1.0, 1.0])

    add_p("Figure 10 visualizes the test RMSE comparison across property crime regression architectures.")
    add_image_fig(r"C:\Users\bbone\Downloads\crime_project\crime_project\outputs\figures\fig_reg_rmse.png", "Figure 10: Test RMSE comparison of regression models")

    # 4.9 Logistic Regression
    add_h2("4.9 Logistic Regression (Classifying High Murder Risk)")
    add_h3("(i) Introduction")
    add_p(
        "From this section onward, the target is binary classification: determining whether a district falls into the high-murder "
        "risk category (high_murder = 1). Logistic regression serves as the fundamental probabilistic linear classifier."
    )
    add_h3("(ii) General Description")
    add_p(
        "Logistic regression maps a linear combination of input predictors to a bounded posterior probability between 0 and 1 via "
        "the standard logistic sigmoid function. Features were standardized using StandardScaler fitted exclusively on the training set."
    )
    add_h3("(iii) Specific Requirements, Functions and Formulas")
    add_p("Using scikit-learn's LogisticRegression(max_iter=1000), the formulations are:")
    add_p(
        "P(y=1|x) = 1 / [ 1 + e^(−(β₀ + βᵀ x)) ]\nLog Loss = −(1/n) Σ [ yᵢ ln(pᵢ) + (1 − yᵢ) ln(1 − pᵢ) ]",
        bold_prefix="Sigmoid and Cross-Entropy Loss: "
    )
    add_h3("(iv) Analysis Results")
    add_p(
        "On the unseen test data, Logistic Regression achieved Accuracy = 86.75%, Precision = 0.8667, Recall = 0.8667, F1-Score = 0.8667, "
        "Log Loss = 0.2863, and ROC-AUC = 0.9528. Five-fold cross-validation confirmed robust generalization with mean CV accuracy = 81.44%. "
        "The model correctly caught 65 out of 75 high-risk districts, missing only 10, while generating only 10 false alarms out of 76 low-risk districts."
    )
    add_p("Python Code (Program 8: Logistic regression)", bold_prefix="")
    code_p8 = (
        'from sklearn.linear_model import LogisticRegression\n'
        'from sklearn.preprocessing import StandardScaler\n'
        'from sklearn.metrics import accuracy_score, log_loss, roc_auc_score, f1_score\n'
        '\n'
        'scaler = StandardScaler()\n'
        'x_tr_sc = scaler.fit_transform(x_train)\n'
        'x_te_sc = scaler.transform(x_test)\n'
        '\n'
        'clf = LogisticRegression(max_iter=1000).fit(x_tr_sc, y_train)\n'
        'y_pred = clf.predict(x_te_sc)\n'
        'y_prob = clf.predict_proba(x_te_sc)[:, 1]\n'
        'print(f"Acc: {accuracy_score(y_test, y_pred):.4f}, AUC: {roc_auc_score(y_test, y_prob):.4f}, F1: {f1_score(y_test, y_pred):.4f}")\n'
    )
    add_code_block(code_p8)
    add_h3("(v) Visualization")
    add_p("The confusion matrix and ROC curve for Logistic Regression are presented in Figures 14 and 15 in Section 4.14.")

    # 4.10 K-Nearest Neighbours
    add_h2("4.10 K-Nearest Neighbours (kNN)")
    add_h3("(i) Introduction")
    add_p(
        "K-Nearest Neighbours is an instance-based non-parametric classifier that classifies new districts based on the majority "
        "class of their nearest neighbors in the multidimensional crime space."
    )
    add_h3("(ii) General Description")
    add_p(
        "kNN relies on Euclidean distance; consequently, feature scaling is mandatory. Hyperparameter tuning was performed across "
        "odd values of k from 1 to 21 to find the optimal bias-variance tradeoff."
    )
    add_h3("(iii) Specific Requirements, Functions and Formulas")
    add_p("Using KNeighborsClassifier(n_neighbors=k) with Euclidean metric:")
    add_p("d(a, b) = √[ Σᵢ (aᵢ − bᵢ)² ]", bold_prefix="Euclidean Distance: ")
    add_h3("(iv) Analysis Results")
    add_p(
        "Testing k across [1, 3, 5, 7, 9, 11, 15, 21] revealed that k = 5 achieved peak performance. On test data, kNN (k=5) achieved "
        "Accuracy = 86.75%, Precision = 0.8767, Recall = 0.8533, F1-Score = 0.8649, Log Loss = 0.7458, and ROC-AUC = 0.9306. "
        "Figure 11 illustrates the tuning curve across k values."
    )
    add_image_fig(r"C:\Users\bbone\Downloads\crime_project\crime_project\outputs\figures\fig_knn_k.png", "Figure 11: Choosing k for the kNN classifier")

    # 4.11 Gaussian Naive Bayes
    add_h2("4.11 Gaussian Naive Bayes")
    add_h3("(i) Introduction")
    add_p(
        "Gaussian Naive Bayes is a fast probabilistic classifier that applies Bayes' theorem with the assumption that input features "
        "follow normal distributions and are conditionally independent given the class label."
    )
    add_h3("(ii) General Description & Formulas")
    add_p(
        "P(y=c|x) ∝ P(y=c) ∏ᵢ P(xᵢ|y=c)\nwhere P(xᵢ|y=c) is evaluated using the Gaussian probability density function.",
        bold_prefix="Bayes Formulation: "
    )
    add_h3("(iv) Analysis Results")
    add_p(
        "Naive Bayes achieved Test Accuracy = 79.47%, Precision = 0.8667, Recall = 0.6933, F1-Score = 0.7704, and ROC-AUC = 0.9011. "
        "This represented the lowest recall (0.6933) and highest log loss (2.2622) among all classifiers. The underlying reason was "
        "established in Section 4.1: violent crime features violate the conditional independence assumption through strong pairwise "
        "multicollinearity (e.g., attempt to murder, dacoity, riots), leading to overconfident misclassifications."
    )

    # 4.12 Decision Tree
    add_h2("4.12 Decision Tree Classifier")
    add_h3("(i) Introduction")
    add_p(
        "Decision trees recursively partition the feature space based on axis-aligned orthogonal splits, providing direct rule-based "
        "interpretability for law enforcement practitioners."
    )
    add_h3("(ii) General Description & Formulas")
    add_p(
        "The model used DecisionTreeClassifier(max_depth=3, random_state=42) using Gini impurity:\nGini = 1 − Σ pᵢ²\n"
        "where pᵢ is the proportion of class i in a node. Limiting tree depth to 3 prevents complex branching and overfitting.",
        bold_prefix="Gini Formulation: "
    )
    add_h3("(iv) Analysis Results")
    add_p(
        "The decision tree achieved Test Accuracy = 84.11%, Precision = 0.8592, Recall = 0.8133, F1-Score = 0.8356, and ROC-AUC = 0.8994. "
        "Feature importance analysis revealed that Attempt to Murder is by far the single most influential determinant (importance = 0.741), "
        "followed by Kidnapping and Abduction (0.158) and Hurt / Grievous Hurt (0.101). Figure 12 plots the feature importance."
    )
    add_image_fig(r"C:\Users\bbone\Downloads\crime_project\crime_project\outputs\figures\fig_dt_importance.png", "Figure 12: Feature importance of the decision tree classifier")
    add_p("Figure 13 displays the complete decision tree architecture with decision thresholds and class purities.")
    add_image_fig(r"C:\Users\bbone\Downloads\crime_project\crime_project\outputs\figures\9_decision_tree.png", "Figure 13: Decision tree structure for high murder risk", width=Inches(6.2))

    # 4.13 Support Vector Machine
    add_h2("4.13 Support Vector Machine (SVM)")
    add_h3("(i) Introduction")
    add_p(
        "Support Vector Machines construct maximum-margin hyperplanes in high-dimensional feature space, employing kernel transformations "
        "to discover nonlinear separation boundaries."
    )
    add_h3("(ii) General Description & Formulas")
    add_p(
        "Using SVC(probability=True, random_state=42), three kernels were evaluated: linear, polynomial, and Radial Basis Function (RBF):\n"
        "K(x, z) = exp( −γ ||x − z||² )",
        bold_prefix="RBF Kernel Formulation: "
    )
    add_h3("(iv) Analysis Results")
    add_p(
        "Kernel evaluation yielded test accuracies of: linear = 85.43%, poly = 81.46%, and RBF = 86.09%. The RBF kernel achieved peak "
        "performance with Test Accuracy = 86.09%, Precision = 0.8649, Recall = 0.8533, F1-Score = 0.8591, Log Loss = 0.3059, "
        "and ROC-AUC = 0.9423, demonstrating strong, robust generalization matching Logistic Regression."
    )

    # 4.14 Master Comparison of Classification Models
    add_h2("4.14 Master Comparison of the Classification Models")
    add_p(
        "All five classification algorithms along with the naive majority-class baseline were rigorously benchmarked on the identical "
        "151 test districts. Table 15 summarizes the comprehensive performance metrics."
    )

    t15_headers = ["Classification Model", "Test Accuracy", "Log Loss", "ROC-AUC", "Precision", "Recall", "F1-Score", "5-Fold CV Acc"]
    t15_rows = [
        ["Baseline (Majority)", "0.5033", "0.6931", "0.5000", "0.0000", "0.0000", "0.0000", "0.5013"],
        ["Logistic Regression", "0.8675", "0.2863", "0.9528", "0.8667", "0.8667", "0.8667", "0.8144"],
        ["KNN (k=5)", "0.8675", "0.7458", "0.9306", "0.8767", "0.8533", "0.8649", "0.7892"],
        ["SVM (RBF Kernel)", "0.8609", "0.3059", "0.9423", "0.8649", "0.8533", "0.8591", "0.8144"],
        ["Decision Tree (d=3)", "0.8411", "0.4090", "0.8994", "0.8592", "0.8133", "0.8356", "0.7467"],
        ["Gaussian Naive Bayes", "0.7947", "2.2622", "0.9011", "0.8667", "0.6933", "0.7704", "0.7866"]
    ]
    add_custom_table(t15_headers, t15_rows, "Table 15: Master performance comparison of the classification models", [1.8, 0.9, 0.9, 0.9, 0.8, 0.8, 0.8, 1.0])

    add_p("Figure 14 displays the confusion matrices of all five classification models side by side.")
    add_image_fig(r"C:\Users\bbone\Downloads\crime_project\crime_project\outputs\figures\fig_confusion_matrices.png", "Figure 14: Confusion matrices of the five classification models", width=Inches(6.2))

    add_p("Figure 15 illustrates the comparative Receiver Operating Characteristic (ROC) curves across all models.")
    add_image_fig(r"C:\Users\bbone\Downloads\crime_project\crime_project\outputs\figures\10_roc_curves.png", "Figure 15: ROC curves of the classification models")

    add_p("Figure 16 compares the F1-scores attained by the classification models.")
    add_image_fig(r"C:\Users\bbone\Downloads\crime_project\crime_project\outputs\figures\fig_f1_scores.png", "Figure 16: F1 score comparison of the classification models")

    # -------------------------------------------------------------
    # CHAPTER 5: CONCLUSION
    # -------------------------------------------------------------
    add_h1("5. Conclusion")

    add_h2("5.1 Summary of the Work")
    add_p(
        "In this project, district-level crime patterns across India were investigated using official 2013 NCRB records (data.gov.in) "
        "to formulate data-driven predictive tools for law enforcement planning. The raw dataset containing 823 rows was systematically "
        "audited and preprocessed by removing 35 statewide total rows ('ZZ TOTAL') that caused 100% double-counting, and eliminating "
        "34 specialized railway and CID policing units. The resulting pristine dataset of 754 verified districts was analyzed through "
        "bivariate correlations, One-way ANOVA across six geographic zones, two-sample t-tests, and Chi-Square contingency testing. "
        "Three regression models and five classification algorithms were constructed, tuned, and evaluated on unseen test data."
    )

    add_h2("5.2 Results of the Models")
    add_p(
        "In regression modeling, property crime prediction demonstrated that quadratic polynomial regression (degree 2) outperformed "
        "both the mean baseline (RMSE = 716.87) and simple linear regression (RMSE = 591.49), achieving test RMSE = 585.90 and R² = 0.3319. "
        "Multiple linear regression with analytical OLS closed-form derivation successfully modeled district murder counts from seven "
        "violent crime categories, achieving an R² of 0.6075 and test MAE of 17.70."
    )
    add_p(
        "In classification modeling, Logistic Regression achieved the highest overall performance, tied in accuracy with kNN at 86.75% "
        "while delivering superior calibration (Log Loss = 0.2863, ROC-AUC = 0.9528, F1-Score = 0.8667). The RBF Support Vector Machine "
        "exhibited nearly identical performance (Accuracy = 86.09%, AUC = 0.9423, F1 = 0.8591). The pruned Decision Tree (depth = 3) "
        "attained 84.11% accuracy while providing complete rule-based transparency. Gaussian Naive Bayes was the weakest classifier (F1 = 0.7704) "
        "due to violated independence assumptions."
    )

    add_h2("5.3 Achievement of the Objectives")
    add_p("All objectives established in Chapter 1 were fully achieved, as summarized in Table 16.")

    t16_headers = ["Project Objective", "Target Benchmark / Criterion", "Quantitative Result Achieved", "Status"]
    t16_rows = [
        ["Data Cleaning & Preprocessing", "Remove double-counting & non-district units", "823 raw rows converted to 754 clean districts (0 nulls)", "Achieved"],
        ["Statistical Hypothesis Testing", "Verify regional & zonal significance (p < 0.05)", "ANOVA F = 29.38, t = -7.85, Chi2 = 70.63 (all p < 0.0001)", "Achieved"],
        ["Continuous Crime Regression", "Outperform naive mean baseline in RMSE & R²", "Theft RMSE reduced from 716.87 to 585.90; Murder R² = 0.6075", "Achieved"],
        ["Risk Classification Modeling", "Substantially exceed 50.3% majority baseline", "Logistic Regression Accuracy = 86.75%, AUC = 0.9528, F1 = 0.8667", "Achieved"],
        ["Comparative Model Benchmarking", "Evaluate all models on identical test partition", "Complete synthesis across 8 diagnostic metrics, ROC & CM", "Achieved"]
    ]
    add_custom_table(t16_headers, t16_rows, "Table 16: Objectives of the project and the results achieved", [2.0, 2.0, 2.2, 0.8])

    add_h2("5.4 Limitations")
    add_p("The findings and models are subject to four recognized limitations:")
    add_bullet(
        "Cross-Sectional Data Restriction: The dataset covers only calendar year 2013; longitudinal dynamic forecasting across future years "
        "requires multi-year panel datasets.",
        bold_prefix="1. Single Temporal Window: "
    )
    add_bullet(
        "Absence of Population Denominators: Incident counts are raw absolute numbers; per-capita rates could not be calculated due to the lack "
        "of synchronized census population counts in the NCRB table.",
        bold_prefix="2. Unadjusted Counts: "
    )
    add_bullet(
        "Inter-State Reporting Variations: Differences in FIR registration propensities across state police administrations influence recorded crime volumes.",
        bold_prefix="3. Administrative Reporting Bias: "
    )
    add_bullet(
        "Linear Independence in Probabilistic Models: High multicollinearity among violent crimes degraded Naive Bayes performance.",
        bold_prefix="4. Multicollinearity Constraints: "
    )

    # -------------------------------------------------------------
    # CHAPTER 6: FUTURE SCOPE
    # -------------------------------------------------------------
    add_h1("6. Future Scope")
    add_p("The foundational methodologies established in this project can be expanded across several promising directions:")
    add_bullet(
        "Multi-Year Longitudinal Panel Analysis: Integrating annual NCRB records from 2001 through 2022 to construct spatio-temporal autoregressive "
        "and sequence models (e.g., ARIMA, LSTM, GRU) for multi-year forecasting.",
        bold_prefix="1. Longitudinal Forecasting: "
    )
    add_bullet(
        "Demographic Normalization: Merging Census of India district demographic, economic, and educational variables to model crime rates per "
        "100,000 population, eliminating population-scale distortions.",
        bold_prefix="2. Demographic Normalization: "
    )
    add_bullet(
        "Geospatial GIS & Spatial Autocorrelation: Incorporating geographic shapefiles and spatial econometrics (Moran's I, spatial lag models) "
        "to map crime spillovers across contiguous district borders.",
        bold_prefix="3. Spatial Econometrics: "
    )
    add_bullet(
        "Advanced Ensemble & Deep Learning: Exploring gradient-boosted ensembles (XGBoost, LightGBM, CatBoost) and TabNet neural architectures "
        "to model complex nonlinear crime interactions.",
        bold_prefix="4. Ensemble Architectures: "
    )
    add_bullet(
        "Operational Decision Support Dashboard: Embedding the best-performing models (Logistic Regression and Decision Tree rules) into an interactive "
        "web-based GIS dashboard for district police commissioners.",
        bold_prefix="5. Decision Support Deployment: "
    )

    # -------------------------------------------------------------
    # CHAPTER 7: REFERENCES
    # -------------------------------------------------------------
    add_h1("7. References")

    refs = [
        "[1] National Crime Records Bureau (2013). Crime in India 2013: Compendium of Crime Statistics. Ministry of Home Affairs, Government of India, New Delhi.",
        "[2] Open Government Data (OGD) Platform India (2013). District-wise IPC Crimes 2013. Ministry of Electronics and Information Technology, Government of India. Available at: https://data.gov.in/",
        "[3] Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research, 12, 2825 – 2830.",
        "[4] McKinney, W. (2010). Data Structures for Statistical Computing in Python. Proceedings of the 9th Python in Science Conference, 56 – 61.",
        "[5] Harris, C. R. et al. (2020). Array programming with NumPy. Nature, 585, 357 – 362.",
        "[6] Virtanen, P. et al. (2020). SciPy 1.0: fundamental algorithms for scientific computing in Python. Nature Methods, 17, 261 – 272.",
        "[7] Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. Computing in Science & Engineering, 9(3), 90 – 95.",
        "[8] Waskom, M. L. (2021). seaborn: statistical data visualization. Journal of Open Source Software, 6(60), 3021.",
        "[9] Hastie, T., Tibshirani, R. and Friedman, J. (2009). The Elements of Statistical Learning: Data Mining, Inference, and Prediction, 2nd edition. Springer, New York.",
        "[10] James, G., Witten, D., Hastie, T. and Tibshirani, R. (2021). An Introduction to Statistical Learning with Applications in Python. Springer, New York.",
        "[11] Hosmer, D. W., Lemeshow, S. and Sturdivant, R. X. (2013). Applied Logistic Regression, 3rd edition. Wiley, Hoboken.",
        "[12] Cover, T. and Hart, P. (1967). Nearest neighbor pattern classification. IEEE Transactions on Information Theory, 13(1), 21 – 27.",
        "[13] Breiman, L., Friedman, J., Olshen, R. and Stone, C. (1984). Classification and Regression Trees. Wadsworth, Belmont.",
        "[14] Cortes, C. and Vapnik, V. (1995). Support-vector networks. Machine Learning, 20, 273 – 297.",
        "[15] Fawcett, T. (2006). An introduction to ROC analysis. Pattern Recognition Letters, 27(8), 861 – 874.",
        "[16] Brantingham, P. J. and Brantingham, P. L. (1984). Patterns in Crime. Macmillan, New York.",
        "[17] Weisburd, D. et al. (2009). The Criminology of Place: Street Segments and Our Understanding of the Crime Problem. Oxford University Press, Oxford."
    ]

    for ref in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_before = Pt(2)
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.paragraph_format.line_spacing = 1.15
        r = p_ref.add_run(ref)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10.5)

    doc.save(output_path)
    print(f"Generated DOCX: {output_path}")

if __name__ == "__main__":
    generate_docx(output_path=r"C:\Users\bbone\Downloads\crime_project\Indian_Crime_Prediction_Report.docx")
