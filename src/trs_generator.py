"""
IFS .trs Translation File Generator
Generates translation files with P: and A:Prompt entries
"""

from typing import Dict, Any, List
from pathlib import Path


class TRSGenerator:
    """Generator for IFS .trs translation files"""
    
    # Language mappings
    LANGUAGES = {
        'sv-SE': {'code': 'sv', 'name': 'Swedish'},
        'nb-NO': {'code': 'no', 'name': 'Norwegian'}
    }
    
    def __init__(self, module: str, layer: str, language: str, main_type: str = "LU", sub_type: str = "Logical Unit"):
        self.module = module
        self.layer = layer
        self.language = language
        self.main_type = main_type
        self.sub_type = sub_type
        
        # Get language code (e.g., 'sv' from 'sv-SE')
        if language in self.LANGUAGES:
            self.lang_code = self.LANGUAGES[language]['code']
            self.culture = language
        else:
            # Assume format like 'sv-SE'
            self.lang_code = language.split('-')[0]
            self.culture = language
    
    def generate_header(self) -> str:
        """Generate .trs file header"""
        header = [
            "-------------------------------------------------------",
            "File Type: IFS Foundation Translation File",
            "Type version: 10.00",
            "-------------------------------------------------------",
            f"Module: {self.module}",
            f"Language: {self.lang_code}",
            f"Culture: {self.culture}",
            f"Layer: {self.layer}",
            f"Main Type: {self.main_type}",
            f"Sub Type: {self.sub_type}",
            "Content: ",
            "-------------------------------------------------------"
        ]
        return '\r\n'.join(header) + '\r\n'
    
    def generate_content(self, data: Dict[str, Any], translations: Dict[str, str]) -> str:
        """
        Generate complete .trs file content
        
        Args:
            data: Parsed and filtered data structure
            translations: Dictionary mapping English labels to translated labels
            
        Returns:
            Complete .trs file content as string
        """
        lines = []
        
        # Process each logical unit
        for lu_id, lu_data in data['logical_units'].items():
            lu_lines = self._generate_lu_block(lu_data, translations, indent_level=0)
            lines.extend(lu_lines)
        
        return ''.join(lines)
    
    def _generate_lu_block(self, lu_data: Dict[str, Any], translations: Dict[str, str], indent_level: int) -> List[str]:
        """Generate CS/CE block for a Logical Unit"""
        lines = []
        indent = '\t' * indent_level
        
        # CS line for LU (no flags in .trs)
        lu_name = lu_data['name']
        lines.append(f"{indent}CS:{lu_name}^LU\r\n")
        
        # Process views
        for view_id, view_data in lu_data['views'].items():
            view_lines = self._generate_view_block(view_data, translations, indent_level + 1)
            lines.extend(view_lines)
        
        # CE line for LU
        lines.append(f"{indent}CE:\r\n")
        
        return lines
    
    def _generate_view_block(self, view_data: Dict[str, Any], translations: Dict[str, str], indent_level: int) -> List[str]:
        """Generate CS/CE block for a View"""
        lines = []
        indent = '\t' * indent_level
        
        # CS line for View (no flags in .trs)
        view_control = view_data['control']
        lines.append(f"{indent}CS:{view_control}^LU\r\n")
        
        # Process columns (only custom fields)
        for col_id, col_data in view_data['columns'].items():
            if col_data['is_custom']:
                col_lines = self._generate_column_block(col_data, translations, indent_level + 1)
                lines.extend(col_lines)
        
        # CE line for View
        lines.append(f"{indent}CE:\r\n")
        
        return lines
    
    def _generate_column_block(self, col_data: Dict[str, Any], translations: Dict[str, str], indent_level: int) -> List[str]:
        """Generate CS/CE block for a Column"""
        lines = []
        indent = '\t' * indent_level
        
        # CS line for Column (no flags in .trs)
        col_control = col_data['control']
        lines.append(f"{indent}CS:{col_control}^LU\r\n")
        
        # P: line for original English text
        original_label = col_data['label']
        lines.append(f"{indent}\tP:{original_label}^\r\n")
        
        # A:Prompt for translated text
        translated_label = translations.get(original_label, original_label)
        lines.append(f"{indent}\tA:Prompt^{translated_label}^\r\n")
        
        # CE line for Column
        lines.append(f"{indent}CE:\r\n")
        
        return lines
    
    def generate_file(self, data: Dict[str, Any], translations: Dict[str, str], output_path: str) -> str:
        """
        Generate complete .trs file
        
        Args:
            data: Parsed and filtered data structure
            translations: Dictionary mapping English labels to translated labels
            output_path: Path to write the file
            
        Returns:
            Path to generated file
        """
        header = self.generate_header()
        content = self.generate_content(data, translations)
        
        full_content = header + content
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            f.write(full_content)
        
        return str(output_file)
    
    def get_file_name(self, module: str, layer: str, language: str) -> str:
        """
        Get standard file name for .trs file
        
        Args:
            module: Module name (e.g., ESSPRO)
            layer: Layer name (e.g., Cust)
            language: Language code (e.g., sv-SE)
            
        Returns:
            File name (e.g., Esspro_LU_LogicalUnit-Cust-sv.trs)
        """
        # Capitalize first letter, rest lowercase for module
        module_formatted = module.capitalize()
        
        # Get language code
        if language in self.LANGUAGES:
            lang_code = self.LANGUAGES[language]['code']
        else:
            lang_code = language.split('-')[0]
        
        return f"{module_formatted}_LU_LogicalUnit-{layer}-{lang_code}.trs"


if __name__ == '__main__':
    # Test the generator
    test_data = {
        'module': 'ESSPRO',
        'layer': 'Cust',
        'logical_units': {
            'TestLU': {
                'name': 'TestLU',
                'label': 'Test Logical Unit',
                'views': {
                    'TEST_VIEW': {
                        'control': 'TEST_VIEW',
                        'label': 'Test View',
                        'columns': {
                            'C_TEST_FIELD': {
                                'control': 'C_TEST_FIELD',
                                'label': 'Test Field',
                                'is_custom': True
                            }
                        }
                    }
                }
            }
        }
    }
    
    test_translations = {
        'Test Field': 'Testfält'
    }
    
    generator = TRSGenerator('ESSPRO', 'Cust', 'sv-SE')
    content = generator.generate_header() + generator.generate_content(test_data, test_translations)
    print(content)
