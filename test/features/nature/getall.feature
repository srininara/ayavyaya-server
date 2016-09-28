Feature: Get All Expense Natures

    Scenario: Get all expense natures
        Given I set header "Content-Type" with value "application/json"
        When I send a GET request to "/natures"
        Then the response code should be 200
        And the response should contain json:
          """
          {
            "natures": [
              {
                "description": "Must have. A required expense.",
                "id": 1,
                "name": "Necessity"
              },
              {
                "description": "An useful expense. Helps to move things forward in terms of income or something similar.",
                "id": 2,
                "name": "Progressive"
              },
              {
                "description": "An expense for convenience",
                "id": 3,
                "name": "Convenience"
              },
              {
                "description": "An expense for luxury and fun",
                "id": 4,
                "name": "Luxury"
              },
              {
                "description": "An useless expense. Things to cover up mistakes, clean up etc.",
                "id": 5,
                "name": "Wasteful"
              },
              {
                "description": "Data Not Available",
                "id": -1000,
                "name": "Not Available"
              }
            ]
          }
          """
