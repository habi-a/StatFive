import React from 'react';
import { LogBox } from 'react-native'
import { createStackNavigator } from 'react-navigation-stack';
import { createAppContainer } from 'react-navigation';

import HomeScreen from './src/home/home.js';
import LoginScreen from './src/login/login.js';
import RegisterScreen from './src/register/register.js';
import StatGameScreen from './src/statgame/statgame.js';
import ProfilScreen from './src/profil/profil.js';
import LeaderBoardScreen from './src/leaderboard/leaderboard.js';

export default class App extends React.Component {

  render() {
    return (
      <Root />
    );
  }
}

const RootStack = createStackNavigator({
  Home: {
    screen: HomeScreen,
  },
  Login: {
    screen: LoginScreen,
  },
  Register: {
    screen: RegisterScreen,
  },
  StatGame: {
    screen: StatGameScreen,
  },
  Profil: {
    screen: ProfilScreen,
  },
  LeaderBoard: {
    screen: LeaderBoardScreen,
  },
},{
  initialRouteName: 'Home',
  headerMode: 'none',
});

LogBox.ignoreAllLogs(true)

const Root = createAppContainer(RootStack);
