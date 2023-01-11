create_complex = {
    "parameters": [
        {
            "in": "body",
            "name": "body",
            "description": "Complex data.",
            "required": True,
            "schema": {
                "$ref": "#/definitions/complex_create"
            }
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
        },
        "complex_create": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string"
                },
                "phone": {
                    "type": "string"
                },
                "address": {
                    "type": "string"
                },
            }
        }
    },
    "responses": {
        "201": {
            "description": "Complex save.",
            "schema": {
                "$ref": "#/definitions/message"
            },
            "examples": {
            }
        }
    }
}

make_admin = {
    "parameters": [
        {
            "in": "path",
            "name": "id",
            "required": True,
        },
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
        },
        "users_update": {
            "type": "object",
            "properties": {
                "post": {
                    "type": "string"
                },
                "description": {
                    "type": "string"
                },
            }
        }
    },
    "responses": {
        "404": {
            "description": "Le compte n\'existe pas.",
            "schema": {
                "$ref": "#/definitions/message"
            },
            "examples": {
            }
        },
        "200": {
            "description": "make-admin.",
            "schema": {
                "$ref": "#/definitions/message"
            },
            "examples": {
            }
        }
    }
}

user_to_complex = {
    "parameters": [
        {
            "in": "path",
            "name": "id",
            "required": True,
        },
        {
            "in": "path",
            "name": "complex_id",
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
        },
        "users_update": {
            "type": "object",
            "properties": {
                "post": {
                    "type": "string"
                },
                "description": {
                    "type": "string"
                },
            }
        }
    },
    "responses": {
        "404": {
            "description": "Le compte n\'existe pas.",
            "schema": {
                "$ref": "#/definitions/message"
            },
            "examples": {
            }
        },
        "200": {
            "description": "make-admin.",
            "schema": {
                "$ref": "#/definitions/message"
            },
            "examples": {
            }
        }
    }
}

user_del_complex = {
    "parameters": [
        {
            "in": "path",
            "name": "id",
            "required": True,
        },
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
        },
        "users_update": {
            "type": "object",
            "properties": {
                "post": {
                    "type": "string"
                },
                "description": {
                    "type": "string"
                },
            }
        }
    },
    "responses": {
        "404": {
            "description": "Le compte n\'existe pas.",
            "schema": {
                "$ref": "#/definitions/message"
            },
            "examples": {
            }
        },
        "200": {
            "description": "user-dissociate-complex.",
            "schema": {
                "$ref": "#/definitions/message"
            },
            "examples": {
            }
        }
    }
}

all_complex = {
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
      "description": "All complex.",
      "schema": {
        "$ref": "#/definitions/message"
      },
      "examples": {
      }
    }
  }
}