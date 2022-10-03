"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
exports.httpClient = undefined;

var _axios = require("axios");

var _axios2 = _interopRequireDefault(_axios);

var _asyncStorage = require("@react-native-async-storage/async-storage");

var _asyncStorage2 = _interopRequireDefault(_asyncStorage);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var httpClient = exports.httpClient = _axios2.default.create({
    //baseURL: "https://api.preprod.statfive.fr/api",
    baseURL: process.env.API_URL ? process.env.API_URL : "https://api.statfive.fr/api"
});

httpClient.interceptors.request.use(async function (config) {
    var token = await _asyncStorage2.default.getItem('token');
    config.headers['api-token'] = token ? token : '';
    return config;
});