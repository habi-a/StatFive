create = {
  "parameters": [
      {
          "in": "body",
          "name": "body",
          "description": "User data.",
          "required": True,
          "schema": {
              "$ref": "#/definitions/users_create"
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
    "users_create": {
      "type": "object",
      "properties": {
        "email": {
          "type": "string"
        },
        "lastname": {
          "type": "string"
        },
        "firstname": {
          "type": "string"
        },
        "password": {
          "type": "string"
        },
      }
    }
  },
  "responses": {
    "400": {
      "description": "Email déjà existant, veuillez en choisir un autre.",
      "schema": {
        "$ref": "#/definitions/message"
      },
      "examples": {
      }
    },
    "201": {
      "description": "Utilisateur bien enregistré.",
      "schema": {
        "$ref": "#/definitions/message"
      },
      "examples": {
      }
    }
  }
}


login = {
  "parameters": [
      {
          "in": "body",
          "name": "body",
          "description": "User data.",
          "required": True,
          "schema": {
              "$ref": "#/definitions/users_login"
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
    "users_login": {
      "type": "object",
      "properties": {
        "email": {
          "type": "string"
        },
        "password": {
          "type": "string"
        }
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
    "401": {
      "description": "Le compte n\'existe pas.",
      "schema": {
        "$ref": "#/definitions/message"
      },
      "examples": {
      }
    },
    "200": {
      "description": "Utilisateur bien login.",
      "schema": {
        "$ref": "#/definitions/message"
      },
      "examples": {
      }
    }
  }
}

user_by_id = {
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
      "description": "Le compte n\'existe pas.",
      "schema": {
        "$ref": "#/definitions/message"
      },
      "examples": {
      }
    },
    "200": {
      "description": "Utilisateur by id.",
      "schema": {
        "$ref": "#/definitions/message"
      },
      "examples": {
      }
    }
  }
}


user_by_name = {
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
      "description": "Le compte n\'existe pas.",
      "schema": {
        "$ref": "#/definitions/message"
      },
      "examples": {
      }
    },
    "200": {
      "description": "Utilisateur by name.",
      "schema": {
        "$ref": "#/definitions/message"
      },
      "examples": {
      }
    }
  }
}


all_user = {
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
      "description": "All user.",
      "schema": {
        "$ref": "#/definitions/message"
      },
      "examples": {
      }
    }
  }
}


stat_user_by_id = {
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
      "description": "Le compte n\'existe pas.",
      "schema": {
        "$ref": "#/definitions/message"
      },
      "examples": {
      }
    },
    "200": {
      "description": "Liste de stats by user id.",
      "schema": {
        "$ref": "#/definitions/message"
      },
      "examples": {
      }
    }
  }
}


verification_code = {
  "parameters": [
      {
          "in": "path",
          "name": "code",
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
    "400": {
      "description": "Code pas bon.",
      "schema": {
        "$ref": "#/definitions/message"
      },
      "examples": {
      }
    },
    "200": {
      "description": "Code bon.",
      "schema": {
        "$ref": "#/definitions/message"
      },
      "examples": {
      }
    }
  }
}