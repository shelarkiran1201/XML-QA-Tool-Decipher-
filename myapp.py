import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import docx
import xml.etree.ElementTree as ET
from xml.dom import minidom
import pandas as pd
import re
from datetime import datetime
import os
from typing import Dict, List, Tuple, Optional
import traceback
import html

class SurveyQAValidator:
    def __init__(self, root):
        self.root = root
        self.root.title("Decipher Survey QA Validator")
        self.root.geometry("900x700")
        self.root.configure(bg='#1e1e1e')
        
        # File paths
        self.word_file = None
        self.xml_file = None
        
        # Data storage
        self.word_questions = []
        self.xml_questions = []
        self.validation_results = []
        
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg='#1e1e1e')
        title_frame.pack(pady=20)
        
        title = tk.Label(title_frame, text="Decipher Survey QA Validator", 
                        font=('Segoe UI', 20, 'bold'), bg='#1e1e1e', fg='#ffffff')
        title.pack()
        
        subtitle = tk.Label(title_frame, text="Word Questionnaire vs XML Programming Validation", 
                           font=('Segoe UI', 10), bg='#1e1e1e', fg='#888888')
        subtitle.pack()
        
        # File Upload Section
        upload_frame = tk.Frame(self.root, bg='#2d2d2d', padx=20, pady=20)
        upload_frame.pack(padx=40, pady=10, fill='x')
        
        # Word File
        word_frame = tk.Frame(upload_frame, bg='#2d2d2d')
        word_frame.pack(fill='x', pady=5)
        
        tk.Label(word_frame, text="Word Document:", font=('Segoe UI', 10), 
                bg='#2d2d2d', fg='#ffffff', width=15, anchor='w').pack(side='left')
        
        self.word_label = tk.Label(word_frame, text="No file selected", 
                                   font=('Segoe UI', 9), bg='#2d2d2d', fg='#888888')
        self.word_label.pack(side='left', padx=10, fill='x', expand=True)
        
        word_btn = tk.Button(word_frame, text="Browse", command=self.browse_word,
                            bg='#007acc', fg='#ffffff', font=('Segoe UI', 9),
                            padx=15, pady=5, relief='flat', cursor='hand2')
        word_btn.pack(side='right')
        
        # XML File
        xml_frame = tk.Frame(upload_frame, bg='#2d2d2d')
        xml_frame.pack(fill='x', pady=5)
        
        tk.Label(xml_frame, text="XML Document:", font=('Segoe UI', 10), 
                bg='#2d2d2d', fg='#ffffff', width=15, anchor='w').pack(side='left')
        
        self.xml_label = tk.Label(xml_frame, text="No file selected", 
                                 font=('Segoe UI', 9), bg='#2d2d2d', fg='#888888')
        self.xml_label.pack(side='left', padx=10, fill='x', expand=True)
        
        xml_btn = tk.Button(xml_frame, text="Browse", command=self.browse_xml,
                           bg='#007acc', fg='#ffffff', font=('Segoe UI', 9),
                           padx=15, pady=5, relief='flat', cursor='hand2')
        xml_btn.pack(side='right')
        
        # Start Button
        btn_frame = tk.Frame(self.root, bg='#1e1e1e')
        btn_frame.pack(pady=15)
        
        self.start_btn = tk.Button(btn_frame, text="Start Validation", 
                                   command=self.start_validation,
                                   bg='#0e639c', fg='#ffffff', 
                                   font=('Segoe UI', 11, 'bold'),
                                   padx=40, pady=10, relief='flat', 
                                   cursor='hand2', state='disabled')
        self.start_btn.pack()
        
        # Progress Section
        progress_frame = tk.Frame(self.root, bg='#2d2d2d', padx=20, pady=15)
        progress_frame.pack(padx=40, pady=10, fill='x')
        
        self.progress_label = tk.Label(progress_frame, text="Ready to start validation", 
                                       font=('Segoe UI', 9), bg='#2d2d2d', fg='#ffffff')
        self.progress_label.pack(anchor='w', pady=(0, 5))
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate', length=400)
        self.progress_bar.pack(fill='x')
        
        # Log Section
        log_frame = tk.Frame(self.root, bg='#2d2d2d', padx=20, pady=15)
        log_frame.pack(padx=40, pady=10, fill='both', expand=True)
        
        tk.Label(log_frame, text="Validation Log:", font=('Segoe UI', 10, 'bold'), 
                bg='#2d2d2d', fg='#ffffff').pack(anchor='w', pady=(0, 5))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, 
                                                  bg='#1e1e1e', fg='#ffffff',
                                                  font=('Consolas', 9), 
                                                  insertbackground='#ffffff')
        self.log_text.pack(fill='both', expand=True)
        
        # Configure progressbar style
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TProgressbar", background='#007acc', troughcolor='#3c3c3c', 
                       bordercolor='#2d2d2d', lightcolor='#007acc', darkcolor='#007acc')
    
    def browse_word(self):
        filename = filedialog.askopenfilename(
            title="Select Word Document",
            filetypes=[("Word Documents", "*.docx"), ("All Files", "*.*")]
        )
        if filename:
            self.word_file = filename
            self.word_label.config(text=os.path.basename(filename), fg='#4ec9b0')
            self.log(f"✓ Word document loaded: {os.path.basename(filename)}")
            self.check_ready()
    
    def browse_xml(self):
        filename = filedialog.askopenfilename(
            title="Select XML Document",
            filetypes=[("XML Files", "*.xml"), ("All Files", "*.*")]
        )
        if filename:
            self.xml_file = filename
            self.xml_label.config(text=os.path.basename(filename), fg='#4ec9b0')
            self.log(f"✓ XML document loaded: {os.path.basename(filename)}")
            self.check_ready()
    
    def check_ready(self):
        if self.word_file and self.xml_file:
            self.start_btn.config(state='normal', bg='#0e7c3d')
    
    def log(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def start_validation(self):
        self.start_btn.config(state='disabled')
        self.progress_bar.start(10)
        self.progress_label.config(text="Validation in progress...")
        self.log("\n" + "="*60)
        self.log("Starting validation process...")
        self.log("="*60)
        
        # Run validation in separate thread
        thread = threading.Thread(target=self.run_validation)
        thread.start()
    
    def run_validation(self):
        try:
            # Parse documents
            self.log("\n[1/5] Parsing Word document...")
            self.parse_word_document()
            self.log(f"✓ Found {len(self.word_questions)} questions in Word document")
            
            self.log("\n[2/5] Parsing XML document...")
            self.parse_xml_document()
            self.log(f"✓ Found {len(self.xml_questions)} questions in XML document")
            
            self.log("\n[3/5] Performing cross-validation...")
            self.validate_questions()
            
            self.log("\n[4/5] Generating validation report...")
            output_file = self.generate_report()
            
            self.log("\n[5/5] Validation complete!")
            self.log(f"✓ Report saved to: {output_file}")
            
            # Show summary
            passed = sum(1 for r in self.validation_results if r['Status'] == 'TRUE')
            failed = len(self.validation_results) - passed
            self.log(f"\n{'='*60}")
            self.log(f"SUMMARY: {passed} passed, {failed} failed out of {len(self.validation_results)} questions")
            self.log(f"{'='*60}")
            
            self.root.after(0, lambda: self.validation_complete(output_file))
            
        except Exception as e:
            error_msg = f"Error during validation: {str(e)}\n{traceback.format_exc()}"
            self.log(f"\n❌ {error_msg}")
            self.root.after(0, lambda: messagebox.showerror("Validation Error", str(e)))
            self.root.after(0, self.reset_ui)
    
    def parse_word_document(self):
        """Parse Word document and extract questions"""
        self.word_questions = []
        doc = docx.Document(self.word_file)
        
        current_question = None
        question_sequence = 0
        
        for para in doc.paragraphs:
            text = para.text.strip()
            if not text:
                continue
            
            # Detect question label (e.g., Q1., AGE., etc.)
            question_match = re.match(r'^([A-Z0-9_]+)\.?\s*(.*)', text)
            if question_match and self.is_likely_question_label(question_match.group(1)):
                if current_question:
                    self.word_questions.append(current_question)
                
                question_sequence += 1
                label = question_match.group(1)
                question_text = question_match.group(2)
                
                current_question = {
                    'label': label,
                    'sequence': question_sequence,
                    'text': question_text,
                    'instruction': '',
                    'options': [],
                    'type': None,
                    'formatting': self.extract_formatting(para)
                }
            elif current_question:
                # Check for instructions
                lower_text = text.lower()
                if any(instr in lower_text for instr in ['select one', 'select all', 'enter a number', 
                                                          'be specific', 'rank', 'drag and drop']):
                    current_question['instruction'] = text
                    current_question['type'] = self.determine_question_type(text)
                else:
                    # Likely an option
                    current_question['options'].append({
                        'text': text,
                        'formatting': self.extract_formatting(para)
                    })
        
        if current_question:
            self.word_questions.append(current_question)
    
    def is_likely_question_label(self, text):
        """Determine if text is likely a question label"""
        # Question labels are typically: Q1, Q2, AGE, GENDER, etc.
        return len(text) <= 20 and (text.startswith('Q') or text.isupper())
    
    def determine_question_type(self, instruction):
        """Determine question type from instruction text"""
        lower = instruction.lower()
        if 'select one' in lower and 'row' in lower:
            return 'radio_grid'
        elif 'select one' in lower:
            return 'radio'
        elif 'select all' in lower and 'row' in lower:
            return 'checkbox_grid'
        elif 'select all' in lower:
            return 'checkbox'
        elif 'enter a number' in lower:
            return 'number'
        elif 'be specific' in lower or 'be as specific' in lower:
            return 'text'
        elif 'rank' in lower or 'drag and drop' in lower:
            return 'ranksort'
        elif 'drop-down' in lower or 'dropdown' in lower:
            return 'dropdown'
        return 'unknown'
    
    def extract_formatting(self, paragraph):
        """Extract formatting information from paragraph"""
        formatting = {
            'bold': False,
            'italic': False,
            'underline': False
        }
        
        for run in paragraph.runs:
            if run.bold:
                formatting['bold'] = True
            if run.italic:
                formatting['italic'] = True
            if run.underline:
                formatting['underline'] = True
        
        return formatting
    
    def clean_xml_content(self, content):
        """Clean and fix common XML issues"""
        lines = content.split('\n')
        cleaned_lines = []
        
        for i, line in enumerate(lines, 1):
            # Skip empty lines
            if not line.strip():
                cleaned_lines.append(line)
                continue
            
            # Fix unescaped ampersands outside of entities and CDATA
            # Don't touch content inside CDATA sections
            if '<![CDATA[' not in line and ']]>' not in line:
                # Replace standalone & with &amp; but preserve entities like &lt; &gt; &amp; etc.
                line = re.sub(r'&(?!(amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)', '&amp;', line)
            
            # Fix unescaped < and > in attribute values
            # This is a simplified fix - may need more sophisticated handling
            if '="' in line or "='" in line:
                # Find attribute values and escape < >
                line = re.sub(r'(<[^>]+)(\s+\w+=["\'])(.*?)(["\'])', 
                             lambda m: m.group(1) + m.group(2) + 
                             m.group(3).replace('<', '&lt;').replace('>', '&gt;') + 
                             m.group(4), line)
            
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def parse_xml_document(self):
        """Parse XML document and extract questions - handles Decipher format with advanced error recovery"""
        self.xml_questions = []
        
        # Read the file content
        with open(self.xml_file, 'r', encoding='utf-8', errors='ignore') as f:
            xml_content = f.read()
        
        # Try multiple parsing strategies
        root = None
        parsing_method = "unknown"
        
        # Strategy 1: Try standard parsing
        try:
            tree = ET.parse(self.xml_file)
            root = tree.getroot()
            parsing_method = "standard"
            self.log("  Using standard XML parsing")
        except ET.ParseError as e:
            self.log(f"  Standard parsing failed: {str(e)}")
            
            # Strategy 2: Clean the XML and try again
            try:
                self.log("  Attempting to clean and fix XML issues...")
                cleaned_content = self.clean_xml_content(xml_content)
                root = ET.fromstring(cleaned_content)
                parsing_method = "cleaned"
                self.log("  ✓ XML issues fixed and parsed successfully")
            except ET.ParseError as e2:
                self.log(f"  Cleaned parsing failed: {str(e2)}")
                
                # Strategy 3: Wrap in root element (Decipher compatibility mode)
                try:
                    self.log("  Applying Decipher XML compatibility mode...")
                    
                    # Remove XML declaration if present
                    xml_lines = xml_content.split('\n')
                    if xml_lines and xml_lines[0].strip().startswith('<?xml'):
                        xml_lines = xml_lines[1:]
                    
                    clean_content = '\n'.join(xml_lines)
                    cleaned_content = self.clean_xml_content(clean_content)
                    wrapped_xml = f'<root>\n{cleaned_content}\n</root>'
                    
                    root = ET.fromstring(wrapped_xml)
                    parsing_method = "wrapped"
                    self.log("  ✓ Successfully parsed using compatibility mode")
                except ET.ParseError as e3:
                    # Strategy 4: Show detailed error information
                    self.log(f"  All parsing strategies failed")
                    self.log(f"  Error: {str(e3)}")
                    
                    # Extract line number from error
                    error_match = re.search(r'line (\d+)', str(e3))
                    if error_match:
                        error_line = int(error_match.group(1))
                        self.log(f"\n  Problematic area around line {error_line}:")
                        lines = xml_content.split('\n')
                        start = max(0, error_line - 3)
                        end = min(len(lines), error_line + 2)
                        for i in range(start, end):
                            marker = " >>> " if i == error_line - 1 else "     "
                            self.log(f"{marker}{i+1}: {lines[i][:100]}")
                    
                    raise Exception(f"Unable to parse XML file. {str(e3)}")
        
        if root is None:
            raise Exception("Failed to parse XML document")
        
        question_sequence = 0
        
        # Find all question elements
        for elem in root.iter():
            if elem.tag in ['radio', 'checkbox', 'text', 'textarea', 'number', 'select', 'html']:
                question_sequence += 1
                label = elem.get('label', '')
                
                question = {
                    'label': label,
                    'sequence': question_sequence,
                    'type': elem.tag,
                    'element': elem,
                    'attributes': elem.attrib,
                    'title': '',
                    'comment': '',
                    'rows': [],
                    'cols': [],
                    'choices': []
                }
                
                # Extract title
                title_elem = elem.find('title')
                if title_elem is not None:
                    question['title'] = self.get_element_text(title_elem)
                
                # Extract comment
                comment_elem = elem.find('comment')
                if comment_elem is not None:
                    question['comment'] = self.get_element_text(comment_elem)
                
                # Extract rows, cols, choices
                for row in elem.findall('row'):
                    question['rows'].append({
                        'label': row.get('label', ''),
                        'text': self.get_element_text(row),
                        'value': row.get('value', '')
                    })
                
                for col in elem.findall('col'):
                    question['cols'].append({
                        'label': col.get('label', ''),
                        'text': self.get_element_text(col),
                        'value': col.get('value', '')
                    })
                
                for choice in elem.findall('choice'):
                    question['choices'].append({
                        'label': choice.get('label', ''),
                        'text': self.get_element_text(choice),
                        'value': choice.get('value', '')
                    })
                
                self.xml_questions.append(question)
    
    def get_element_text(self, element):
        """Extract text content from XML element, preserving formatting tags"""
        if element.text:
            return ''.join(element.itertext()).strip()
        return ''
    
    def validate_questions(self):
        """Perform validation between Word and XML questions"""
        self.validation_results = []
        
        # Create lookup dictionaries
        word_dict = {q['label']: q for q in self.word_questions}
        xml_dict = {q['label']: q for q in self.xml_questions}
        
        # Get all unique labels
        all_labels = set(word_dict.keys()) | set(xml_dict.keys())
        
        for label in sorted(all_labels):
            word_q = word_dict.get(label)
            xml_q = xml_dict.get(label)
            
            result = {
                'Word Question Label': label if word_q else '',
                'XML Question Label': label if xml_q else '',
                'Present in Word': 'Yes' if word_q else 'No',
                'Present in XML': 'Yes' if xml_q else 'No',
                'Sequence Status': '',
                'Word Sequence Position': word_q['sequence'] if word_q else '',
                'XML Sequence Position': xml_q['sequence'] if xml_q else '',
                'Status': 'TRUE',
                'Error Description': ''
            }
            
            errors = []
            
            # Check presence
            if not word_q:
                errors.append(f"Question '{label}' exists in XML but not in Word document")
                result['Status'] = 'FALSE'
            elif not xml_q:
                errors.append(f"Question '{label}' exists in Word but not in XML document")
                result['Status'] = 'FALSE'
            else:
                # Both exist - perform detailed validation
                
                # Check sequence
                if word_q['sequence'] != xml_q['sequence']:
                    errors.append(f"Sequence mismatch: Word position {word_q['sequence']}, XML position {xml_q['sequence']}")
                    result['Sequence Status'] = 'Out of Sequence'
                    result['Status'] = 'FALSE'
                else:
                    result['Sequence Status'] = 'Correct'
                
                # Validate question type
                type_errors = self.validate_question_type(word_q, xml_q)
                if type_errors:
                    errors.extend(type_errors)
                    result['Status'] = 'FALSE'
                
                # Validate text content
                text_errors = self.validate_text_content(word_q, xml_q)
                if text_errors:
                    errors.extend(text_errors)
                    result['Status'] = 'FALSE'
                
                # Validate formatting
                format_errors = self.validate_formatting(word_q, xml_q)
                if format_errors:
                    errors.extend(format_errors)
                    result['Status'] = 'FALSE'
            
            result['Error Description'] = '; '.join(errors) if errors else 'All validations passed'
            self.validation_results.append(result)
    
    def validate_question_type(self, word_q, xml_q):
        """Validate that XML question type matches Word question type"""
        errors = []
        
        word_type = word_q.get('type')
        xml_type = xml_q.get('type')
        
        # Map XML types to expected types
        type_mapping = {
            'radio': ['radio', 'radio_grid'],
            'checkbox': ['checkbox', 'checkbox_grid'],
            'number': ['number'],
            'text': ['text'],
            'textarea': ['text'],
            'select': ['dropdown', 'ranksort'],
            'html': ['descriptive']
        }
        
        if word_type and xml_type:
            expected_types = type_mapping.get(xml_type, [])
            if word_type not in expected_types and word_type != 'unknown':
                errors.append(f"Question type mismatch: Word indicates '{word_type}', XML is '{xml_type}'")
        
        return errors
    
    def validate_text_content(self, word_q, xml_q):
        """Validate text content matches between Word and XML"""
        errors = []
        
        # Normalize text for comparison
        def normalize(text):
            if not text:
                return ''
            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text.strip())
            # Remove trailing period from question labels only
            text = re.sub(r'\.$', '', text)
            # Remove [X] or [x] markers
            text = re.sub(r'\[x\]|\[X\]', '', text, flags=re.IGNORECASE)
            return text.strip()
        
        # Compare question text/title
        word_text = normalize(word_q.get('text', ''))
        xml_title = normalize(xml_q.get('title', ''))
        
        if word_text and xml_title and word_text != xml_title:
            errors.append(f"Question text mismatch: Word='{word_text[:50]}...', XML='{xml_title[:50]}...'")
        
        # Compare instruction/comment
        word_instruction = normalize(word_q.get('instruction', ''))
        xml_comment = normalize(xml_q.get('comment', ''))
        
        if word_instruction and xml_comment and word_instruction != xml_comment:
            errors.append(f"Instruction text mismatch: Word='{word_instruction[:50]}...', XML='{xml_comment[:50]}...'")
        
        return errors
    
    def validate_formatting(self, word_q, xml_q):
        """Validate formatting matches between Word and XML"""
        errors = []
        
        # Check if Word question has formatting
        word_fmt = word_q.get('formatting', {})
        
        # Check XML title for formatting tags
        xml_title = xml_q.get('title', '')
        
        has_bold_tag = '<b>' in xml_title or '<strong>' in xml_title
        has_italic_tag = '<i>' in xml_title or '<em>' in xml_title
        has_underline_tag = '<u>' in xml_title
        
        if word_fmt.get('bold') and not has_bold_tag:
            errors.append("Missing bold formatting in XML title")
        
        if word_fmt.get('italic') and not has_italic_tag:
            errors.append("Missing italic formatting in XML title")
        
        if word_fmt.get('underline') and not has_underline_tag:
            errors.append("Missing underline formatting in XML title")
        
        return errors
    
    def generate_report(self):
        """Generate Excel report with validation results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"QA_Validation_Report_{timestamp}.xlsx"
        
        df = pd.DataFrame(self.validation_results)
        
        # Create Excel writer with formatting
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Validation Results', index=False)
            
            # Auto-adjust column widths
            worksheet = writer.sheets['Validation Results']
            for idx, col in enumerate(df.columns):
                max_length = max(df[col].astype(str).apply(len).max(), len(col)) + 2
                worksheet.column_dimensions[chr(65 + idx)].width = min(max_length, 50)
        
        return output_file
    
    def validation_complete(self, output_file):
        self.progress_bar.stop()
        self.progress_label.config(text="Validation complete!")
        self.start_btn.config(state='normal', bg='#0e7c3d')
        
        messagebox.showinfo("Validation Complete", 
                          f"Validation completed successfully!\n\nReport saved to:\n{output_file}")
    
    def reset_ui(self):
        self.progress_bar.stop()
        self.progress_label.config(text="Ready to start validation")
        self.start_btn.config(state='normal', bg='#0e7c3d')

def main():
    root = tk.Tk()
    app = SurveyQAValidator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
