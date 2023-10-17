class EndPoint:
    """
    A class to represent a EndPoint(API) in the code.

    Attributes
    ----------
        id : Id of Postman API/EndPoint
        name : Name of Postman API
        authentication : Authentication method of the API
        method : Method of API request (eg. GET, POST, etc.)
        header : header parameters in the request
        url : URL in the API request
        query_parameters : input query parameters
    """

    def __init__(self, end_point_json):

        self.id = end_point_json["uid"]
        self.name = end_point_json["name"]
        self.authentication = end_point_json["request"].get("auth")
        self.method = end_point_json["request"]["method"]
        self.header = end_point_json["request"].get("header")
        self.url = end_point_json["request"]["url"]["raw"]
        self.query_parameters = end_point_json["request"]["url"].get("query")

    def get_id(self):
        """
        Get ID of the API
        """
        return self.id

    def get_name(self):
        """
        Get name of the API
        """
        return self.name

    def get_authentication(self):
        """
        Get authentication type of API
        """
        return self.authentication

    def get_method(self):
        """
        Get method of API request
        """
        return self.method

    def get_header(self):
        """
        Get header in the API request
        """
        return self.header

    def get_url(self):
        """
        Get url of the API request
        """
        return self.url

    def get_query_parameters(self):
        """
        Get query params of the API request
        """
        return self.query_parameters

# end_point_json = {
#     "collection":
#                 {"info":
#                         {"_postman_id":"e9683d9f-2d4d-49c8-af2e-38ecbc55e5fe",
#                          "name":"Mock data generation",
#                          "description":"# \xf0\x9f\x93\x8b Get started here\n\nPostman provides dynamic variables that use the [Faker library](https://www.npmjs.com/package/@faker-js/faker) to generate sample data, including random names, addresses, and email addresses.\n\nThis template demonstrates the use of dynamic variables to create randomized mock data. The examples in this collection utilize various data types and showcase how dynamic variables can help simulate real-world data within your API testing environment.\n\n## \xf0\x9f\x94\x96 How to use this template\n\n**Step 1: Send requests**\n\nSelect a request from the collection, review the request parameters and pre-request scripts, then hit \"Send\" to execute the request.\n\n**Step 2: Review the \"Body\" and \"Pre-request Script\"** **tabs**\n\nUnderstand how dynamic variables are used to generate mock data. Dynamic variables can be used in the request URL and Body, or even as part of a Pre-Request or Test script for more complex use cases (see \"Create mock blog post\" request).\n\n**Step 3: Customize (optional)**\n\nCustomize dynamic variables to better suit your specific use case. Save the changes, and execute the requests.\n\n**Step 4: Analyze responses**\n\nExamine the response body to see the generated mock data. Note that the responses will be different each time you send the request, as the dynamic variables ensure randomized data generation.\n\nEnjoy testing with diverse and dynamic data!\n\n## \xe2\x84\xb9\xef\xb8\x8f Resources\n\n[Dynamic variables](https://learning.postman.com/docs/writing-scripts/script-references/variables-list/)","schema":"https://schema.getpostman.com/json/collection/v2.1.0/collection.json","updatedAt":"2023-10-14T19:21:12.000Z","uid":"29786585-e9683d9f-2d4d-49c8-af2e-38ecbc55e5fe"},"item":[{"name":"Create mock purchase","id":"05ecec4f-cf2b-4163-a59c-f67903fef8bb","request":{"method":"POST","header":[],"body":{"mode":"raw","raw":"{\n    \"userId\": \"{{$guid}}\",\n    \"payment\": {\n        \"cardNumber\": \"{{$randomCreditCardMask}}\",\n        \"currency\": \"{{$randomCurrencyCode}}\",\n        \"amount\": {{$randomInt}},\n        \"confirmed\": \"{{$randomBoolean}}\",\n        \"confirmedAt\": \"{{$isoTimestamp}}\"\n    },\n    \"basket\": [\n        {\n            \"id\": \"{{$guid}}\",\n            \"quantity\": {{$randomInt}}\n        },\n        {\n            \"id\": \"{{$guid}}\",\n            \"quantity\": {{$randomInt}}\n        }\n    ]\n}","options":{"raw":{"language":"json"}}},"url":{"raw":"{{baseUrl}}/post","host":["{{baseUrl}}"],"path":["post"]},"description":"This request shows an example of generating mock purchase details in the request body. It demonstrates a few finance-related dynamic variables, in addition to the ones for random ID, Integer, Boolean, and Timestamp."},"response":[],"uid":"29786585-05ecec4f-cf2b-4163-a59c-f67903fef8bb"},{"name":"Create mock blog post","event":[{"listen":"prerequest","script":{"type":"text/javascript","exec":["// Use a dynamic variable in script","// https://learning.postman.com/docs/writing-scripts/script-references/variables-list/","const loremParagraphs = pm.variables.replaceIn(\"{{$randomLoremParagraphs}}\");","","// $randomLoremParagraphs generates a string with multiple paragraphs separated by ","// newline control characters (\"\\n\"). Since we\'re using this in a JSON object, we ","// need to replace the newline control character with the JSON-safe string \"\\\\n\".","const blogPostContent = loremParagraphs.replace(/\\n/g, \"\\\\n\")","","// Make the result available as a variable for use in the request body","pm.variables.set(\'blogPostContent\', blogPostContent)"]}}],"id":"7747bee0-f59f-42d6-9b00-0634d59cc1a3","request":{"method":"POST","header":[],"body":{"mode":"raw","raw":"{\n    \"author\": \"{{$randomUserName}}\",\n    \"title\": \"{{$randomLoremWords}}\",\n    \"slug\": \"{{$randomLoremSlug}}\",\n    \"summary\": \"{{$randomLoremSentences}}\",\n    \"body\": \"{{blogPostContent}}\"\n}","options":{"raw":{"language":"json"}}},"url":{"raw":"{{baseUrl}}/post","host":["{{baseUrl}}"],"path":["post"]},"description":"This request shows an example of generating longer-form content, in this case, a blog post, and transforming mock data as part of a pre-request script.\n\nIn the body, we use dynamic variables to generate a name, a short set of words as a title, a \'slug\' (URL-safe textual identifier like \"dolores-est-iusto\"), and a post summary.\n\nIn the pre-request script, we generate some paragraphs of text using `pm.variables.replaceIn`. We then transform this text to make it JSON-safe by replacing newline characters with escaped newline characters and setting the result to a variable we can reference in the body."},"response":[],"uid":"29786585-7747bee0-f59f-42d6-9b00-0634d59cc1a3"}],"event":[{"listen":"prerequest","script":{"type":"text/javascript","exec":[""]}},{"listen":"test","script":{"type":"text/javascript","exec":[""]}}],"variable":[{"id":"cd60c7fb-3ba8-4a8f-bf1c-e020627abd8d","key":"baseUrl","value":"https://postman-echo.com","type":"string"}]}}

# print(end_point_json["collection"]["info"]["_postman_id"])
