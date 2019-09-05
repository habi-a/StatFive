import React, { Component } from "react";
import {createStackNavigator, createAppContainer} from 'react-navigation';
import styles from "./style";
import {Keyboard, 
        Text, 
        View, 
        TextInput, 
        TouchableWithoutFeedback, 
        Alert, 
        KeyboardAvoidingView,
        ImageBackground} from 'react-native';
import { Button } from 'react-native-elements';

import annexe from '../../annexe.js';

export default class LoginScreen extends Component {

  static navigationOptions = {
    header:null,
  };

  constructor(props){
    super(props)
    this.state = {
      password: "",
      email: ""
    }
}
  onLoginPress = async () => {
    let body_login = new FormData();
    body_login.append("email", this.state.email)
    body_login.append("password", this.state.password)
    const login = {
      method: "POST",
      'Accept': 'application/json',
      'Content-Type': 'multipart/form-data',
      body:body_login,
    };
    if(this.state.password == "" || this.state.email == "" ) {
        Alert.alert(
          'Champs manquants',
          'Veuillez remplir tout les champs',
        );
    }
    else {
        fetch(annexe.ip+"login", login)
        .then(res => res.json()).then((result) => {
          console.log(result)
          if(result.Connected == true) {
            console.log(result)
            this.props.navigation.navigate('Accueil')
          }
          else {
            Alert.alert(
              'Erreur',
              'E-mail ou Password invalide',
            );
          }
        }).catch((error) => console.log("Erreur Login: " ,error)
        );
      };
  };

  render() {
    return (
    <ImageBackground source={require('../../assets/background-home.png')} style={{width: '100%', height: '100%'}}>
        <KeyboardAvoidingView style={styles.containerView} behavior="padding">
            <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
                <View style={styles.loginScreenContainer}>
                    <View style={styles.loginFormView}>
                        <Text style={styles.logoText}>StatFive</Text>
                        <TextInput placeholder="E-mail" placeholderTextColor="#3897f1" style={styles.loginFormTextInput} onChange={(e) => this.setState({email: e.nativeEvent.text})} />
                        <TextInput placeholder="Mot de Passe" placeholderTextColor="#3897f1" style={styles.loginFormTextInput} secureTextEntry={true} onChange={(e) => this.setState({password: e.nativeEvent.text})} />
                        <Button
                        buttonStyle={styles.loginButton}
                        onPress={() => this.onLoginPress()}
                        title="Connexion"
                        />
                        <View style={styles.MainContainer}>
                            <Text style={styles.TextStyle} onPress={ ()=> this.props.navigation.navigate('Register') }>Pas de compte ?</Text>
                        </View>
                    </View>
                </View>
            </TouchableWithoutFeedback>
        </KeyboardAvoidingView>
    </ImageBackground>
    );
  }
}
