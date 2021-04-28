import React from 'react';
import { createStackNavigator, createAppContainer} from 'react-navigation';

import LoginScreen from './src/login/login.js';
import RegisterScreen from './src/register/register.js';
import AccueilScreen from './src/accueil/accueil.js';
import StatGameScreen from './src/statgame/statgame.js';

export default class App extends React.Component {

  render() {
    return (
      <Root />
    );
  }
}


const RootStack = createStackNavigator({
  Login: { screen: LoginScreen },
  Register: { screen: RegisterScreen},
  Accueil : { screen: AccueilScreen},
  StatGame : { screen: StatGameScreen},

},{
  initialRouteName: 'Login',
  headerMode: 'none',
});

console.disableYellowBox = true;

const Root = createAppContainer(RootStack);
