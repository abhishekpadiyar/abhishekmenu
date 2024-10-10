from flask import Flask, request, jsonify
from flask_cors import CORS
from googlesearch import search  # Import the Google search function


@app.route('/search', methods=['GET'])
def perform_search():
    """Perform a Google search and return the results."""
    query = request.args.get('query', '')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    try:
        # Perform the Google search
        search_results = search(query, num_results=10, lang='en')

        # Return the search results as JSON
        return jsonify({"results": list(search_results)})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


