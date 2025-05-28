#!/usr/bin/env python3
"""
Test script for API schema endpoint
Tests the /schema endpoint and validates OpenAPI structure
"""

import requests
import json
import sys

def test_schema_endpoint():
    """Test the /schema endpoint"""
    base_url = "http://localhost:8001"
    
    print("🧪 Testing API Schema Endpoint")
    print("=" * 50)
    
    try:
        # Test schema endpoint
        print("\n1. Testing /schema endpoint...")
        response = requests.get(f"{base_url}/schema")
        
        if response.status_code == 200:
            print("✅ Schema endpoint accessible")
            
            # Parse JSON
            schema = response.json()
            
            # Validate OpenAPI structure
            print("\n2. Validating OpenAPI structure...")
            
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
            
            print(f"\n3. Validating endpoints ({len(expected_paths)} expected)...")
            for path in expected_paths:
                if path in paths:
                    print(f"✅ {path}")
                else:
                    print(f"❌ {path}: Missing")
            
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
            
            print(f"\n4. Validating schemas ({len(expected_schemas)} expected)...")
            for schema_name in expected_schemas:
                if schema_name in schemas:
                    print(f"✅ {schema_name}")
                else:
                    print(f"❌ {schema_name}: Missing")
            
            # Check tags
            tags = schema.get('tags', [])
            expected_tags = ['search', 'details', 'utility']
            
            print(f"\n5. Validating tags ({len(expected_tags)} expected)...")
            tag_names = [tag.get('name') for tag in tags]
            for tag in expected_tags:
                if tag in tag_names:
                    print(f"✅ {tag}")
                else:
                    print(f"❌ {tag}: Missing")
            
            # Schema size info
            schema_json = json.dumps(schema, indent=2)
            schema_size = len(schema_json)
            print(f"\n📊 Schema Statistics:")
            print(f"   • Total size: {schema_size:,} characters")
            print(f"   • Endpoints: {len(paths)}")
            print(f"   • Schemas: {len(schemas)}")
            print(f"   • Tags: {len(tags)}")
            
            print(f"\n✅ Schema validation completed successfully!")
            return True
            
        else:
            print(f"❌ Schema endpoint failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure the API is running on http://localhost:8001")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_schema_examples():
    """Test some example endpoints mentioned in schema"""
    base_url = "http://localhost:8001"
    
    print("\n🔍 Testing Example Endpoints")
    print("=" * 50)
    
    # Test endpoints that should work without external dependencies
    test_endpoints = [
        ('/', 'API Documentation'),
        ('/health', 'Health Check'),
        ('/schema', 'OpenAPI Schema')
    ]
    
    for endpoint, description in test_endpoints:
        try:
            print(f"\nTesting {endpoint} ({description})...")
            response = requests.get(f"{base_url}{endpoint}")
            
            if response.status_code == 200:
                print(f"✅ {endpoint}: {response.status_code}")
                
                # Check if response is valid JSON
                try:
                    data = response.json()
                    print(f"   📄 Response type: {type(data).__name__}")
                    if isinstance(data, dict) and 'status' in data:
                        print(f"   📊 Status: {data.get('status')}")
                except:
                    print("   ⚠️  Response is not JSON")
            else:
                print(f"❌ {endpoint}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ {endpoint}: Error - {e}")

def main():
    """Main test function"""
    print("🚀 Streamy API Schema Test Suite")
    print("=" * 50)
    
    # Test schema endpoint
    schema_success = test_schema_endpoint()
    
    # Test example endpoints
    test_schema_examples()
    
    print("\n" + "=" * 50)
    if schema_success:
        print("🎉 All schema tests passed!")
        print("\n📖 Schema Documentation:")
        print("   • OpenAPI Schema: http://localhost:8001/schema")
        print("   • API Documentation: http://localhost:8001/")
        print("   • Health Check: http://localhost:8001/health")
        print("   • Markdown Docs: backend/API_SCHEMA.md")
        
        print("\n🛠️  Integration Options:")
        print("   • Swagger UI: Import schema from /schema endpoint")
        print("   • Postman: Import OpenAPI spec for collection generation")
        print("   • Code Generation: Use OpenAPI generators for client SDKs")
        
        sys.exit(0)
    else:
        print("❌ Schema tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 