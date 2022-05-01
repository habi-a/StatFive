all_match = {
  "parameters": [
  ],
  "definitions": {
    "message": {
      "type": "object",
      "properties": {
        "data": {
          "type": "array"
        },
        "message": {
          "type": "string"
        },
        "error": {
          "type": "boolean"
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "All Matchs.",
      "schema": {
        "$ref": "#/definitions/message"
      },
      "examples": {
      }
    }
  }
}

stat_match_by_id = {
  "parameters": [
      {
          "in": "path",
          "name": "id",
          "required": True,
      }
  ],
  "definitions": {
    "message": {
      "type": "object",
      "properties": {
        "message": {
          "type": "string"
        },
        "error": {
          "type": "boolean"
        }
      }
    }
  },
  "responses": {
    "404": {
      "description": "Le match n\'existe pas.",
      "schema": {
        "$ref": "#/definitions/message"
      },
      "examples": {
      }
    },
    "200": {
      "description": "Liste de stats by match id.",
      "schema": {
        "$ref": "#/definitions/message"
      },
      "examples": {
      }
    }
  }
}
