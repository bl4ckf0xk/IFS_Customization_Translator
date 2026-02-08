"""
IFS Language Automation Tool - Main Entry Point
Orchestrates XML parsing, file generation, translation, and validation
"""

import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any

from parser import IFSXMLParser
from lng_generator import LNGGenerator
from trs_generator import TRSGenerator
from translator import IFSTranslator
from validator import IFSValidator
from logger import IFSLogger


class IFSLanguageAutomation:
    """Main automation orchestrator"""
    
    def __init__(self, xml_path: str, output_dir: str = None, languages: List[str] = None, 
                 translation_backend: str = 'dictionary', api_key: str = None):
        self.xml_path = Path(xml_path)
        self.output_dir = Path(output_dir) if output_dir else self.xml_path.parent
        self.languages = languages or ['sv-SE', 'nb-NO']
        
        # Initialize components
        self.logger = IFSLogger(self.output_dir / 'Log.txt')
        self.parser = IFSXMLParser(self.xml_path)
        self.translator = IFSTranslator(backend=translation_backend, api_key=api_key)
        self.validator = IFSValidator()
        
        # Data storage
        self.parsed_data = None
        self.custom_data = None
        self.translations = {}
        
    def run(self):
        """Execute the complete automation workflow"""
        try:
            self.logger.info("=" * 60)
            self.logger.info("IFS Language Automation Tool - Starting")
            self.logger.info("=" * 60)
            
            # Step 1: Parse XML
            self._parse_xml()
            
            # Step 2: Extract custom fields
            self._extract_custom_fields()
            
            # Step 3: Generate .lng file
            self._generate_lng_file()
            
            # Step 4: Translate labels
            self._translate_labels()
            
            # Step 5: Generate .trs files
            self._generate_trs_files()
            
            # Step 6: Validate all files
            self._validate_files()
            
            # Step 7: Write log
            self.logger.info("=" * 60)
            self.logger.info("IFS Language Automation Tool - Completed Successfully")
            self.logger.info("=" * 60)
            self.logger.write_to_file()
            
            print("\n" + "=" * 60)
            print("SUCCESS: All files generated and validated")
            print("=" * 60)
            print(f"\nGenerated files in: {self.output_dir}")
            print(self.logger.get_summary())
            
        except Exception as e:
            self.logger.error(f"Fatal error: {e}")
            self.logger.write_to_file()
            print(f"\nERROR: {e}")
            sys.exit(1)
    
    def _parse_xml(self):
        """Step 1: Parse XML file"""
        self.logger.log_parsing_start(str(self.xml_path))
        
        if not self.xml_path.exists():
            raise FileNotFoundError(f"XML file not found: {self.xml_path}")
        
        self.parsed_data = self.parser.parse()
        stats = self.parser.get_statistics(self.parsed_data)
        
        self.logger.log_parsing_complete(stats)
    
    def _extract_custom_fields(self):
        """Step 2: Extract custom fields (C_* only)"""
        self.logger.info("Extracting custom fields (C_* prefix only)")
        
        self.custom_data = self.parser.extract_custom_fields(self.parsed_data)
        
        # Count custom fields
        custom_count = 0
        for lu_data in self.custom_data['logical_units'].values():
            for view_data in lu_data['views'].values():
                for col_id, col_data in view_data['columns'].items():
                    custom_count += 1
                    self.logger.log_field_processed(col_id, col_data['label'])
        
        self.logger.success(f"Extracted {custom_count} custom fields")
        
        # Log skipped standard fields
        stats = self.parser.get_statistics(self.parsed_data)
        skipped_count = stats['standard_columns']
        if skipped_count > 0:
            self.logger.info(f"Skipped {skipped_count} standard fields (non-C_* prefix)")
    
    def _generate_lng_file(self):
        """Step 3: Generate .lng file"""
        module = self.custom_data['module']
        layer = self.custom_data['layer']
        
        generator = LNGGenerator(module, layer)
        file_name = generator.get_file_name(module, layer)
        output_path = self.output_dir / file_name
        
        self.logger.info(f"Generating .lng file: {file_name}")
        
        generated_file = generator.generate_file(self.custom_data, str(output_path))
        
        self.logger.log_file_generation(generated_file, "Created")
        self.logger.success(f"Generated .lng file: {file_name}")
    
    def _translate_labels(self):
        """Step 4: Translate labels to all target languages"""
        # Collect all unique labels
        labels = set()
        for lu_data in self.custom_data['logical_units'].values():
            for view_data in lu_data['views'].values():
                for col_data in view_data['columns'].values():
                    labels.add(col_data['label'])
        
        labels_list = sorted(list(labels))
        
        # Translate to each language
        for language in self.languages:
            self.logger.log_translation_start(language, len(labels_list))
            
            translations = self.translator.translate_batch(labels_list, language)
            self.translations[language] = translations
            
            self.logger.log_translation_complete(language)
    
    def _generate_trs_files(self):
        """Step 5: Generate .trs files for each language"""
        module = self.custom_data['module']
        layer = self.custom_data['layer']
        
        for language in self.languages:
            generator = TRSGenerator(module, layer, language)
            file_name = generator.get_file_name(module, layer, language)
            output_path = self.output_dir / file_name
            
            self.logger.info(f"Generating .trs file: {file_name}")
            
            translations = self.translations[language]
            generated_file = generator.generate_file(self.custom_data, translations, str(output_path))
            
            self.logger.log_file_generation(generated_file, "Created")
            self.logger.success(f"Generated .trs file: {file_name}")
    
    def _validate_files(self):
        """Step 6: Validate all generated files"""
        module = self.custom_data['module']
        layer = self.custom_data['layer']
        
        # Validate .lng file
        lng_generator = LNGGenerator(module, layer)
        lng_file = self.output_dir / lng_generator.get_file_name(module, layer)
        self._validate_single_file(lng_file)
        
        # Validate .trs files
        for language in self.languages:
            trs_generator = TRSGenerator(module, layer, language)
            trs_file = self.output_dir / trs_generator.get_file_name(module, layer, language)
            self._validate_single_file(trs_file)
    
    def _validate_single_file(self, file_path: Path):
        """Validate a single file"""
        self.logger.log_validation_start(str(file_path))
        
        is_valid, errors, warnings = self.validator.validate_file(str(file_path))
        
        if errors:
            for error in errors:
                self.logger.error(f"  {error}")
            raise ValueError(f"Validation failed for {file_path.name}")
        
        if warnings:
            for warning in warnings:
                self.logger.warning(f"  {warning}")
        
        self.logger.log_validation_success(str(file_path))


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='IFS Language Automation Tool - Generate .lng and .trs files from XML'
    )
    
    parser.add_argument(
        '--xml',
        required=True,
        help='Path to TranslatableResources XML file'
    )
    
    parser.add_argument(
        '--output-dir',
        help='Output directory (default: same as XML file)'
    )
    
    parser.add_argument(
        '--languages',
        default='sv-SE,nb-NO',
        help='Comma-separated list of language codes (default: sv-SE,nb-NO)'
    )
    
    parser.add_argument(
        '--backend',
        choices=['dictionary', 'groq', 'google'],
        default='dictionary',
        help='Translation backend: dictionary (default), groq (AI), or google (Google Translate)'
    )
    
    parser.add_argument(
        '--api-key',
        help='API key for groq or google (can also use GROQ_API_KEY or GOOGLE_API_KEY env var)'
    )
    
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only validate existing files without generating new ones'
    )
    
    args = parser.parse_args()
    
    # Parse languages
    languages = [lang.strip() for lang in args.languages.split(',')]
    
    # Run automation
    automation = IFSLanguageAutomation(
        xml_path=args.xml,
        output_dir=args.output_dir,
        languages=languages,
        translation_backend=args.backend,
        api_key=args.api_key
    )
    
    if args.validate_only:
        print("Validation-only mode not yet implemented")
        sys.exit(1)
    else:
        automation.run()


if __name__ == '__main__':
    main()
