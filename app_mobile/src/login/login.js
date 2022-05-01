import React, { Component } from "react";
import { createStackNavigator } from 'react-navigation-stack';
import { createAppContainer } from 'react-navigation';
import {Keyboard,
        Text,
        View,
        TextInput,
        TouchableWithoutFeedback,
        Alert,
        KeyboardAvoidingView,
        Image,
        ImageBackground} from 'react-native';
import { Button } from 'react-native-elements';

import style from "./style";
import annexe from '../../api_link'

TextInput.defaultProps.selectionColor = '#0090F8'

export default class LoginScreen extends Component {

  static navigationOptions = {
    headerShown:false,
  };

  constructor(props){
    super(props)
    this.state = {
      password: "",
      email: ""
    }
}
  onLoginPress = async () => {
    var myHeaders = new Headers();
    myHeaders.append("Accept", "application/json");
    myHeaders.append("Content-Type", "application/json");
    let body_login = JSON.stringify({
                          "email":this.state.email,
                          "password":this.state.password
                        })

    var login = {
                  method: 'POST',
                  headers: myHeaders,
                  body: body_login,
                };

    if(this.state.password == "" || this.state.email == "" ) {
        Alert.alert(
          'Champs manquants',
          'Veuillez remplir tout les champs',
        );
    }
    else {
        fetch(annexe.ip+"users/login", login)
        .then(res => res.json())
        .then(res => {
          if(res.message == "Utilisateur bien login.") {
            console.log(res)
            Alert.alert(
                ''+res.data.firstname,
                'Nous sommes heureux de vous revoir ',
            );
            this.props.navigation.navigate('Home', {id:res.data.id})
          }
          else {
            Alert.alert(
              'Erreur',
              'L\'E-mail ou le Password est invalide',
            );
          }
        }).catch((error) => console.log("Erreur Login: " ,error));
      };
  };

  render() {
    return (
    //<ImageBackground source={require('../../assets/home.png')} style={{width: '100%', height: '100%'}}>
        <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
            <KeyboardAvoidingView style={style.containerView} behavior="padding">
                <View style={style.loginScreenContainer}>
                    <View style={style.loginFormView}>
                        <Image
                          style={{width: '100%', height: 360, marginBottom: -50}}
                          resizeMode="contain"
                          source={require('../../assets/StatFive.gif')}
                        />
                        <Text></Text>
                        <TextInput placeholder="E-mail" placeholderTextColor="#0090F8" style={style.loginFormTextInput} onChange={(e) => this.setState({email: e.nativeEvent.text})} />
                        <TextInput placeholder="Mot de Passe" placeholderTextColor="#0090F8" style={style.loginFormTextInput} secureTextEntry={true} onChange={(e) => this.setState({password: e.nativeEvent.text})} />
                        <Button
                          buttonStyle={style.loginButton}
                          onPress={() => this.onLoginPress()}
                          title="Connexion"
                        />
                        <View style={style.MainContainer}>
                            <Text style={style.TextStyle} onPress={ ()=> this.props.navigation.navigate('Register') }>Toujours pas inscrit ?</Text>
                        </View>
                    </View>
                </View>
            </KeyboardAvoidingView>
        </TouchableWithoutFeedback>
    //</ImageBackground>
    );
  }
}
