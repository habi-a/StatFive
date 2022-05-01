all_team = {
    "parameters": [
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
        "200": {
            "description": "All teams.",
            "schema": {
                "$ref": "#/definitions/message"
            },
            "examples": {
            }
        }
    }
}

average_team = {
    "parameters": [
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
        "200": {
            "description": "All average_team teams.",
            "schema": {
                "$ref": "#/definitions/message"
            },
            "examples": {
            }
        }
    }
}

team_by_id = {
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
            "description": "La team n\'existe pas.",
            "schema": {
                "$ref": "#/definitions/message"
            },
            "examples": {
            }
        },
        "200": {
            "description": "Team by id.",
            "schema": {
                "$ref": "#/definitions/message"
            },
            "examples": {
            }
        }
    }
}

team_by_name = {
    "parameters": [
        {
            "in": "path",
            "name": "name",
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
            "description": "La team n\'existe pas.",
            "schema": {
                "$ref": "#/definitions/message"
            },
            "examples": {
            }
        },
        "200": {
            "description": "Team by name.",
            "schema": {
                "$ref": "#/definitions/message"
            },
            "examples": {
            }
        }
    }
}

create = {
    "parameters": [
        {
            "in": "body",
            "name": "body",
            "description": "Team data.",
            "required": True,
            "schema": {
                "$ref": "#/definitions/teams_create"
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
        "teams_create": {
            "type": "object",
            "properties": {
                "red": {
                    "type": "string"
                },
                "blue": {
                    "type": "string"
                }
            }
        }
    },
    "responses": {
        "201": {
            "description": "Teams bien enregistré.",
            "schema": {
                "$ref": "#/definitions/message"
            },
            "examples": {
            }
        }
    }
}

stat_team_by_id = {
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
            "description": "La team n\'existe pas.",
            "schema": {
                "$ref": "#/definitions/message"
            },
            "examples": {
            }
        },
        "200": {
            "description": "Team stats by id.",
            "schema": {
                "$ref": "#/definitions/message"
            },
            "examples": {
            }
        }
    }
}