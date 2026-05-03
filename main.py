import requests

# SECTION 1: Fetching Data using the requests Library
# API: JSONPlaceholder (free fake API for testing)

api_url = "https://jsonplaceholder.typicode.com/posts"

# Make a GET request to the API
response = requests.get(api_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    print("Successfully fetched data!")

    # Parse the JSON response
    posts = response.json()
    print(f"Total posts fetched: {len(posts)}")

    print("\nFirst 3 posts:")
    for i, post in enumerate(posts[:3]):
        print(f"Post {i+1}:")
        print(f"  ID: {post['id']}")
        print(f"  Title: {post['title'][:50]}...")   # Display first 50 chars of title
        print(f"  Body: {post['body'][:100]}...")     # Display first 100 chars of body
        print("-" * 20)
else:
    print(f"Error fetching data: {response.status_code} - {response.text}")



# SECTION 2: Applying Filtering / Search Logic

print("\n--- Search & Filter ---")

# Search by keyword in title
keyword = input("\nEnter a keyword to search in post titles (or press Enter to skip): ").strip().lower()

if keyword:
    filtered_by_keyword = [post for post in posts if keyword in post['title'].lower()]
    print(f"\nPosts containing '{keyword}' in title: {len(filtered_by_keyword)} found")
    for i, post in enumerate(filtered_by_keyword[:5]):
        print(f"Post {i+1}:")
        print(f"  ID: {post['id']}")
        print(f"  Title: {post['title'][:50]}...")
        print("-" * 20)
    if not filtered_by_keyword:
        print(f"No posts found with keyword '{keyword}'.")

# Filter posts by userId
user_id_to_filter = 1
filtered_posts_again = [post for post in posts if post['userId'] == user_id_to_filter]

print(f"\nPosts by User ID {user_id_to_filter}: {len(filtered_posts_again)} found")
if filtered_posts_again:
    print("First 3 filtered posts:")
    for i, post in enumerate(filtered_posts_again[:3]):
        print(f"Post {i+1}:")
        print(f"  ID: {post['id']}")
        print(f"  Title: {post['title'][:50]}...")
        print("-" * 20)
else:
    print(f"No posts found for User ID {user_id_to_filter}.")


# SECTION 3: Handling API Errors

def fetch_data_with_error_handling(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        print(f"Successfully fetched data from {url}")
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Status Code: {response.status_code} from {url}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err} - Could not connect to {url}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err} - Request timed out for {url}")
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected error occurred: {req_err} for {url}")
    except ValueError:  # Catches JSON decoding errors
        print(f"Error: Could not decode JSON from response for {url}. Content: {response.text[:100]}...")
    return None


print("\n--- Demonstrating Error Handling ---")

# Scenario 1: Successful request
print("\nAttempting a successful request:")
successful_data = fetch_data_with_error_handling("https://jsonplaceholder.typicode.com/posts/1")
if successful_data:
    print(f"Fetched single post title: {successful_data['title'][:50]}...")

# Scenario 2: Resource Not Found (404 Error)
print("\nAttempting a request for a non-existent resource (expecting 404):")
non_existent_data = fetch_data_with_error_handling("https://jsonplaceholder.typicode.com/nonexistent-endpoint")

# Scenario 3: Connection Error (malformed URL)
print("\nAttempting a request to a malformed URL (expecting Connection Error):")
malformed_url_data = fetch_data_with_error_handling("http://invalid.url.example/test")

# Scenario 4: Note about 5xx
print("\nNote: The `raise_for_status()` method also handles server-side 5xx errors in a similar fashion.")