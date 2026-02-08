"""
IFS .lng File Generator
Generates language files with proper CS/CE block structure
"""

from typing import Dict, Any, List
from pathlib import Path


class LNGGenerator:
    """Generator for IFS .lng language files"""
    
    def __init__(self, module: str, layer: str, main_type: str = "LU", sub_type: str = "Logical Unit"):
        self.module = module
        self.layer = layer
        self.main_type = main_type
        self.sub_type = sub_type
        
    def generate_header(self) -> str:
        """Generate .lng file header"""
        header = [
            "-------------------------------------------------------",
            "File Type: IFS Foundation Language File",
            "Type version: 10.00",
            "-------------------------------------------------------",
            f"Module: {self.module}",
            f"Layer: {self.layer}",
            f"Main Type: {self.main_type}",
            f"Sub Type: {self.sub_type}",
            "Content: ",
            "-------------------------------------------------------"
        ]
        return '\r\n'.join(header) + '\r\n'
    
    def generate_content(self, data: Dict[str, Any]) -> str:
        """
        Generate complete .lng file content
        
        Args:
            data: Parsed and filtered data structure
            
        Returns:
            Complete .lng file content as string
        """
        lines = []
        
        # Process each logical unit
        for lu_id, lu_data in data['logical_units'].items():
            lu_lines = self._generate_lu_block(lu_data, indent_level=0)
            lines.extend(lu_lines)
        
        return ''.join(lines)
    
    def _generate_lu_block(self, lu_data: Dict[str, Any], indent_level: int) -> List[str]:
        """Generate CS/CE block for a Logical Unit"""
        lines = []
        indent = '\t' * indent_level
        
        # CS line for LU
        lu_name = lu_data['name']
        lines.append(f"{indent}CS:{lu_name}^LU^Logical Unit^N^N\r\n")
        
        # A:Prompt for LU
        lu_label = lu_data['label']
        lines.append(f"{indent}\tA:Prompt^{lu_label}^\r\n")
        
        # Process views
        for view_id, view_data in lu_data['views'].items():
            view_lines = self._generate_view_block(view_data, indent_level + 1)
            lines.extend(view_lines)
        
        # CE line for LU
        lines.append(f"{indent}CE:\r\n")
        
        return lines
    
    def _generate_view_block(self, view_data: Dict[str, Any], indent_level: int) -> List[str]:
        """Generate CS/CE block for a View"""
        lines = []
        indent = '\t' * indent_level
        
        # CS line for View
        view_control = view_data['control']
        lines.append(f"{indent}CS:{view_control}^LU^View^N^N\r\n")
        
        # Process columns (only custom fields)
        for col_id, col_data in view_data['columns'].items():
            if col_data['is_custom']:
                col_lines = self._generate_column_block(col_data, indent_level + 1)
                lines.extend(col_lines)
        
        # CE line for View
        lines.append(f"{indent}CE:\r\n")
        
        return lines
    
    def _generate_column_block(self, col_data: Dict[str, Any], indent_level: int) -> List[str]:
        """Generate CS/CE block for a Column"""
        lines = []
        indent = '\t' * indent_level
        
        # CS line for Column
        col_control = col_data['control']
        lines.append(f"{indent}CS:{col_control}^LU^Column^N^N\r\n")
        
        # A:Prompt for Column
        col_label = col_data['label']
        lines.append(f"{indent}\tA:Prompt^{col_label}^\r\n")
        
        # CE line for Column
        lines.append(f"{indent}CE:\r\n")
        
        return lines
    
    def generate_file(self, data: Dict[str, Any], output_path: str) -> str:
        """
        Generate complete .lng file
        
        Args:
            data: Parsed and filtered data structure
            output_path: Path to write the file
            
        Returns:
            Path to generated file
        """
        header = self.generate_header()
        content = self.generate_content(data)
        
        full_content = header + content
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            f.write(full_content)
        
        return str(output_file)
    
    def merge_with_existing(self, new_data: Dict[str, Any], existing_file: str) -> Dict[str, Any]:
        """
        Merge new data with existing .lng file to avoid duplicates
        
        Args:
            new_data: New data to add
            existing_file: Path to existing .lng file
            
        Returns:
            Merged data structure
        """
        # For now, we'll just return new_data
        # In a production system, you'd parse the existing file and merge
        # This is a simplified version since we're creating new files
        return new_data
    
    def get_file_name(self, module: str, layer: str) -> str:
        """
        Get standard file name for .lng file
        
        Args:
            module: Module name (e.g., ESSPRO)
            layer: Layer name (e.g., Cust)
            
        Returns:
            File name (e.g., Esspro_LU_LogicalUnit-Cust.lng)
        """
        # Capitalize first letter, rest lowercase for module
        module_formatted = module.capitalize()
        return f"{module_formatted}_LU_LogicalUnit-{layer}.lng"


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
    
    generator = LNGGenerator('ESSPRO', 'Cust')
    content = generator.generate_header() + generator.generate_content(test_data)
    print(content)
