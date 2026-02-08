"""
IFS TranslatableResources XML Parser
Extracts custom fields (C_* prefix) from XML files
"""

import xml.etree.ElementTree as ET
from typing import Dict, Any, List
from pathlib import Path


class IFSXMLParser:
    """Parser for IFS TranslatableResources XML files"""
    
    NAMESPACE = {'ifs': 'types.scan.translation.fnd.ifsworld.com'}
    
    def __init__(self, xml_path: str):
        self.xml_path = Path(xml_path)
        self.tree = None
        self.root = None
        
    def parse(self) -> Dict[str, Any]:
        """
        Parse XML file and extract structure
        
        Returns:
            Dictionary containing module, layer, and logical unit hierarchy
        """
        self.tree = ET.parse(self.xml_path)
        self.root = self.tree.getroot()
        
        # Extract root attributes
        result = {
            'type': self.root.get('type'),
            'module': self.root.get('module'),
            'version': self.root.get('version'),
            'layer': self.root.get('layer'),
            'logical_units': {}
        }
        
        # Process each TranslatableResource (Logical Unit)
        # Use .// to search recursively and handle any namespace
        for lu_elem in self.root:
            if 'TranslatableResource' in lu_elem.tag:
                lu_data = self._parse_logical_unit(lu_elem)
                if lu_data:
                    lu_id = lu_elem.get('ID')
                    result['logical_units'][lu_id] = lu_data
        
        return result
    
    def _parse_logical_unit(self, lu_elem: ET.Element) -> Dict[str, Any]:
        """Parse a Logical Unit element"""
        lu_data = {
            'id': lu_elem.get('ID'),
            'name': lu_elem.get('name'),
            'type': lu_elem.get('type'),
            'label': self._get_text(lu_elem),
            'views': {}
        }
        
        # Process views - iterate through all children
        for child in lu_elem:
            if 'Resource' in child.tag and child.get('subtype') == 'View':
                view_data = self._parse_view(child)
                if view_data:
                    view_id = child.get('control')
                    lu_data['views'][view_id] = view_data
        
        return lu_data
    
    def _parse_view(self, view_elem: ET.Element) -> Dict[str, Any]:
        """Parse a View element"""
        view_data = {
            'id': view_elem.get('ID'),
            'control': view_elem.get('control'),
            'label': self._get_text(view_elem),
            'columns': {}
        }
        
        # Process columns - iterate through all children
        for child in view_elem:
            if 'Resource' in child.tag and child.get('subtype') == 'Column':
                col_control = child.get('control')
                col_label = self._get_text(child)
                
                # Store all columns (filtering happens later)
                view_data['columns'][col_control] = {
                    'id': child.get('ID'),
                    'control': col_control,
                    'label': col_label,
                    'is_custom': col_control.startswith('C_')
                }
        
        return view_data
    
    def _get_text(self, elem: ET.Element) -> str:
        """Extract text from CDATA section"""
        # Find Text element - iterate through children
        for child in elem:
            if 'Text' in child.tag:
                if child.text:
                    return child.text.strip()
        return ''
    
    def extract_custom_fields(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Filter to only include custom fields (C_* prefix)
        
        Args:
            parsed_data: Full parsed data structure
            
        Returns:
            Filtered data containing only custom fields
        """
        result = {
            'type': parsed_data['type'],
            'module': parsed_data['module'],
            'version': parsed_data['version'],
            'layer': parsed_data['layer'],
            'logical_units': {}
        }
        
        for lu_id, lu_data in parsed_data['logical_units'].items():
            filtered_lu = {
                'id': lu_data['id'],
                'name': lu_data['name'],
                'type': lu_data['type'],
                'label': lu_data['label'],
                'views': {}
            }
            
            for view_id, view_data in lu_data['views'].items():
                # Filter columns to only custom fields
                custom_columns = {
                    col_id: col_data
                    for col_id, col_data in view_data['columns'].items()
                    if col_data['is_custom']
                }
                
                if custom_columns:
                    filtered_lu['views'][view_id] = {
                        'id': view_data['id'],
                        'control': view_data['control'],
                        'label': view_data['label'],
                        'columns': custom_columns
                    }
            
            # Only include LU if it has custom fields
            if filtered_lu['views']:
                result['logical_units'][lu_id] = filtered_lu
        
        return result
    
    def get_statistics(self, parsed_data: Dict[str, Any]) -> Dict[str, int]:
        """Get statistics about parsed data"""
        stats = {
            'total_logical_units': 0,
            'total_views': 0,
            'total_columns': 0,
            'custom_columns': 0,
            'standard_columns': 0
        }
        
        for lu_data in parsed_data['logical_units'].values():
            stats['total_logical_units'] += 1
            for view_data in lu_data['views'].values():
                stats['total_views'] += 1
                for col_data in view_data['columns'].values():
                    stats['total_columns'] += 1
                    if col_data['is_custom']:
                        stats['custom_columns'] += 1
                    else:
                        stats['standard_columns'] += 1
        
        return stats


if __name__ == '__main__':
    # Test the parser
    import sys
    if len(sys.argv) > 1:
        parser = IFSXMLParser(sys.argv[1])
        data = parser.parse()
        custom_data = parser.extract_custom_fields(data)
        stats = parser.get_statistics(data)
        
        print(f"Module: {data['module']}")
        print(f"Layer: {data['layer']}")
        print(f"Statistics: {stats}")
        print(f"\nCustom fields found: {stats['custom_columns']}")
