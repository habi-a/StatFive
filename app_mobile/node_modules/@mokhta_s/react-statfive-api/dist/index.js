"use strict";

var _axiosConfig = require("./axiosConfig");

var _asyncStorage = require("@react-native-async-storage/async-storage");

var _asyncStorage2 = _interopRequireDefault(_asyncStorage);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var axios = require("axios");


var isEmail = function isEmail(val) {
  var regEmail = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  if (!regEmail.test(val)) {
    return true;
  }
};

var login = function login(API_URL, email, password) {
  if (!isEmail(email)) {
    var result = axios.post(API_URL + "/users/login", { email: email, password: password }).then(async function (res) {
      await _asyncStorage2.default.setItem("token", res.data.data.token);
      await _asyncStorage2.default.setItem("userInfo", JSON.stringify(res.data.data));
      return res.data;
    }).catch(function (err) {
      return err.response;
    });
    return result;
  }
  return "L'email n'est pas conforme.";
};

var register = function register(API_URL, email, firstname, lastname, password, pass2) {
  if (password !== pass2) return { error: "Les mots de passe ne correspondent pas" };
  if (lastname.length < 2 || firstname < 2) return { error: "Le prénom ou le nom est trop court" };
  if (!isEmail(email)) {
    var result = axios.post(API_URL + "/users/create", { email: email, firstname: firstname, lastname: lastname, password: password }).then(function (res) {
      return res.data;
    }).catch(function (err) {
      return err.response.data;
    });
    return result;
  }
  return "Une erreur est survenue.";
};

var getAverageGoal = async function getAverageGoal() {
  var result = await _axiosConfig.httpClient.get("/team/average_team").then(function (res) {
    return res.data.data.sort(function (a, b) {
      return b.moyenne_goal - a.moyenne_goal;
    });
    //return res.data.data
  }).catch(function (err) {
    return err.response;
  });
  return result;
};

module.exports = {
  login: login,
  register: register,
  getAverageGoal: getAverageGoal,
  getAllTeam: async function getAllTeam() {
    var result = await _axiosConfig.httpClient.get("/team/all_team").then(function (res) {
      var arrayObj = res.data.data;
      arrayObj = arrayObj.map(function (item) {
        return {
          value: item.id,
          label: item.name
        };
      });
      return arrayObj;
    }).catch(function (err) {
      console.log(err);
      return err.response;
    });
    return result;
  },
  addVideo: async function addVideo(mp4, teamOne, teamTwo) {
    var bodyFormData = new FormData();
    bodyFormData.append("video", mp4);
    bodyFormData.append("team_one", teamOne);
    bodyFormData.append("team_two", teamTwo);

    var headers = {
      "Content-Type": "multipart/form-data",
      "Access-Control-Allow-Origin": "*"
    };
    var result = await _axiosConfig.httpClient.post("/match", bodyFormData, { headers: headers }).then(function (res) {
      return res;
    }).catch(function (err) {
      return err.response;
    });
    return result;
  },
  createTeam: async function createTeam(teamName, arrayTeam) {
    var result = await _axiosConfig.httpClient.post("/team/create_team", [{ name: teamName, player: arrayTeam }]).then(function (res) {
      return res;
    }).catch(function (err) {
      return err.response;
    });
    return result;
  },
  matchListHistoric: async function matchListHistoric() {
    var result = await _axiosConfig.httpClient.get("/match/all_match").then(function (res) {
      return res.data.data;
    }).catch(function (err) {
      return err.response;
    });
    return result;
  },
  updateProfil: async function updateProfil(idUser, description, post) {
    var result = await _axiosConfig.httpClient.put("/users/" + idUser, { description: description, post: post }).then(function (res) {
      return res;
    }).catch(function (err) {
      return err.response;
    });
    return result;
  },
  getTeam: async function getTeam() {
    var result = await _axiosConfig.httpClient.get("/team/all_team").then(function (res) {
      return res.data.data;
    }).catch(function (err) {
      return err.response;
    });
    return result;
  },
  getMyTeam: async function getMyTeam() {
    var result = await _axiosConfig.httpClient.get("/team").then(function (res) {
      return res.data.data;
    }).catch(function (err) {
      return err.response;
    });
    return result;
  },
  verification: async function verification(otp) {
    var result = await _axiosConfig.httpClient.get("/users/verification_code/" + otp.toUpperCase()).then(async function (res) {
      return res;
    }).catch(function (err) {
      return err.response;
    });
    return result;
  },
  getUserInfo: async function getUserInfo(idUser) {
    var result = await _axiosConfig.httpClient.get("/users/" + idUser).then(async function (res) {
      return res;
    }).catch(function (err) {
      return err.response;
    });
    return result;
  },
  statMatchById: async function statMatchById(idMatch) {
    var result = await _axiosConfig.httpClient.get("/match/stat_match_by_id/" + idMatch).then(async function (res) {
      return res;
    }).catch(function (err) {
      return err.response;
    });
    return result;
  },
  getAllUser: async function getAllUser() {
    var result = await _axiosConfig.httpClient.get("/users/all_user").then(function (res) {
      return res;
    }).catch(function (err) {
      return err.response;
    });
    return result;
  },
  getNewPassword: async function getNewPassword(mail) {
    var result = await _axiosConfig.httpClient.post('/users/mail-reset-password', { "email": mail }).then(function (res) {
      return res;
    }).catch(function (err) {
      return err.response;
    });
    return result;
  },
  changeMyPassword: async function changeMyPassword(code, password) {
    var result = await _axiosConfig.httpClient.post('/users/confirm-reset-password', { code: code, password: password }).then(function (res) {
      return res;
    }).catch(function (err) {
      return err.response;
    });
    return result;
  },
  getMe: async function getMe() {
    var result = await _axiosConfig.httpClient.get('/users/me').then(function (res) {
      return res;
    }).catch(function (err) {
      return err.response;
    });
    return result;
  }
};