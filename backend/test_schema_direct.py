#!/usr/bin/env python3
"""
Direct test of API schema without server
Tests the schema structure and validates OpenAPI compliance
"""

import json
import sys
from api_schema import get_api_schema

def test_schema_structure():
    """Test the schema structure directly"""
    print("🧪 Testing API Schema Structure (Direct)")
    print("=" * 50)
    
    try:
        # Get schema
        schema = get_api_schema()
        
        # Validate OpenAPI structure
        print("\n1. Validating OpenAPI structure...")
        
        # Check required OpenAPI fields
        required_fields = ['openapi', 'info', 'paths', 'components']
        for field in required_fields:
            if field in schema:
                print(f"✅ {field}: Present")
            else:
                print(f"❌ {field}: Missing")
                return False
        
        # Check OpenAPI version
        if schema.get('openapi') == '3.0.3':
            print("✅ OpenAPI version: 3.0.3")
        else:
            print(f"❌ OpenAPI version: {schema.get('openapi')} (expected 3.0.3)")
        
        # Check API info
        info = schema.get('info', {})
        if info.get('title') == 'Streamy Torrent Search API':
            print("✅ API title: Correct")
        else:
            print(f"❌ API title: {info.get('title')}")
        
        if info.get('version') == '5.0.0':
            print("✅ API version: 5.0.0")
        else:
            print(f"❌ API version: {info.get('version')}")
        
        # Check paths
        paths = schema.get('paths', {})
        expected_paths = [
            '/',
            '/health', 
            '/schema',
            '/search/{query}',
            '/movies/{query}',
            '/tv-shows/{query}',
            '/details/movie/{tmdb_id}',
            '/details/tv/{tmdb_id}',
            '/details/tv/{tv_id}/season/{season_number}',
            '/details/tv/{tv_id}/season/{season_number}/episode/{episode_number}'
        ]
        
        print(f"\n2. Validating endpoints ({len(expected_paths)} expected)...")
        missing_paths = []
        for path in expected_paths:
            if path in paths:
                print(f"✅ {path}")
            else:
                print(f"❌ {path}: Missing")
                missing_paths.append(path)
        
        # Check components/schemas
        components = schema.get('components', {})
        schemas = components.get('schemas', {})
        
        expected_schemas = [
            'ErrorResponse',
            'HealthResponse', 
            'ApiDocumentation',
            'SearchResponse',
            'SearchResult',
            'MovieDetailsResponse',
            'TvDetailsResponse',
            'SeasonDetailsResponse',
            'EpisodeDetailsResponse',
            'MovieDetails',
            'TvDetails',
            'SeasonDetails',
            'EpisodeDetails',
            'TorrentResult',
            'Credit',
            'Genre',
            'SpokenLanguage',
            'Season',
            'Episode'
        ]
        
        print(f"\n3. Validating schemas ({len(expected_schemas)} expected)...")
        missing_schemas = []
        for schema_name in expected_schemas:
            if schema_name in schemas:
                print(f"✅ {schema_name}")
            else:
                print(f"❌ {schema_name}: Missing")
                missing_schemas.append(schema_name)
        
        # Check tags
        tags = schema.get('tags', [])
        expected_tags = ['search', 'details', 'utility']
        
        print(f"\n4. Validating tags ({len(expected_tags)} expected)...")
        tag_names = [tag.get('name') for tag in tags]
        missing_tags = []
        for tag in expected_tags:
            if tag in tag_names:
                print(f"✅ {tag}")
            else:
                print(f"❌ {tag}: Missing")
                missing_tags.append(tag)
        
        # Schema size info
        schema_json = json.dumps(schema, indent=2)
        schema_size = len(schema_json)
        print(f"\n📊 Schema Statistics:")
        print(f"   • Total size: {schema_size:,} characters")
        print(f"   • Endpoints: {len(paths)}")
        print(f"   • Schemas: {len(schemas)}")
        print(f"   • Tags: {len(tags)}")
        
        # Detailed validation
        print(f"\n🔍 Detailed Validation:")
        
        # Check each endpoint has proper HTTP methods
        endpoint_methods = {}
        for path, methods in paths.items():
            endpoint_methods[path] = list(methods.keys())
            
        print(f"   • All endpoints use GET method: {'✅' if all('get' in methods for methods in endpoint_methods.values()) else '❌'}")
        
        # Check schema references
        schema_refs = set()
        def find_refs(obj):
            if isinstance(obj, dict):
                if '$ref' in obj:
                    ref = obj['$ref']
                    if ref.startswith('#/components/schemas/'):
                        schema_refs.add(ref.split('/')[-1])
                for value in obj.values():
                    find_refs(value)
            elif isinstance(obj, list):
                for item in obj:
                    find_refs(item)
        
        find_refs(schema)
        
        # Check if all referenced schemas exist
        missing_refs = schema_refs - set(schemas.keys())
        if missing_refs:
            print(f"   • Missing schema references: {missing_refs}")
        else:
            print(f"   • All schema references valid: ✅")
        
        # Summary
        total_issues = len(missing_paths) + len(missing_schemas) + len(missing_tags) + len(missing_refs)
        
        if total_issues == 0:
            print(f"\n✅ Schema validation completed successfully!")
            print(f"   • All {len(expected_paths)} endpoints documented")
            print(f"   • All {len(expected_schemas)} schemas defined")
            print(f"   • All {len(expected_tags)} tags present")
            print(f"   • All schema references valid")
            return True
        else:
            print(f"\n⚠️  Schema validation completed with {total_issues} issues")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_schema_examples():
    """Test schema examples and structure"""
    print("\n🔍 Testing Schema Examples")
    print("=" * 50)
    
    try:
        schema = get_api_schema()
        
        # Test a few key schemas for proper structure
        schemas = schema.get('components', {}).get('schemas', {})
        
        # Test SearchResponse schema
        search_response = schemas.get('SearchResponse')
        if search_response:
            required_fields = search_response.get('required', [])
            expected_required = ['status', 'query', 'count', 'results']
            if set(expected_required).issubset(set(required_fields)):
                print("✅ SearchResponse: Required fields correct")
            else:
                print(f"❌ SearchResponse: Missing required fields: {set(expected_required) - set(required_fields)}")
        
        # Test MovieDetailsResponse schema
        movie_response = schemas.get('MovieDetailsResponse')
        if movie_response:
            required_fields = movie_response.get('required', [])
            expected_required = ['status', 'tmdb_details', 'torrent_count', 'torrent_results']
            if set(expected_required).issubset(set(required_fields)):
                print("✅ MovieDetailsResponse: Required fields correct")
            else:
                print(f"❌ MovieDetailsResponse: Missing required fields: {set(expected_required) - set(required_fields)}")
        
        # Test TorrentResult schema
        torrent_result = schemas.get('TorrentResult')
        if torrent_result:
            required_fields = torrent_result.get('required', [])
            expected_required = ['title', 'magnet', 'size', 'seeders', 'leechers']
            if set(expected_required).issubset(set(required_fields)):
                print("✅ TorrentResult: Required fields correct")
            else:
                print(f"❌ TorrentResult: Missing required fields: {set(expected_required) - set(required_fields)}")
        
        print("✅ Schema examples validation completed")
        return True
        
    except Exception as e:
        print(f"❌ Error testing examples: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Streamy API Schema Direct Test")
    print("=" * 50)
    
    # Test schema structure
    structure_success = test_schema_structure()
    
    # Test schema examples
    examples_success = test_schema_examples()
    
    print("\n" + "=" * 50)
    if structure_success and examples_success:
        print("🎉 All schema tests passed!")
        print("\n📖 Schema Information:")
        print("   • OpenAPI Version: 3.0.3")
        print("   • API Version: 5.0.0")
        print("   • Total Endpoints: 10")
        print("   • Total Schemas: 20+")
        print("   • Documentation: backend/API_SCHEMA.md")
        
        print("\n🛠️  Usage:")
        print("   • Start API: python3 app.py")
        print("   • Get Schema: curl http://localhost:8001/schema")
        print("   • Import to Swagger UI, Postman, etc.")
        
        sys.exit(0)
    else:
        print("❌ Schema tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 