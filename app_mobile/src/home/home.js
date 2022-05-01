import React, { Component } from "react";
import { createStackNavigator } from 'react-navigation-stack';
import { createAppContainer } from 'react-navigation';
import { List, ListItem } from 'native-base';
import {Keyboard,
        Text,
        View,
        TouchableWithoutFeedback,
        KeyboardAvoidingView,
        RefreshControl,
        TouchableOpacity,
        AsyncStorage,
        Image,
        ImageBackground,
        Alert } from 'react-native';
import { ScrollView } from "react-native-gesture-handler";
import Icon from 'react-native-vector-icons/FontAwesome';

import style from "./style";
import annexe from '../../api_link'

export default class HomeScreen extends Component {

    static navigationOptions = {
      headerShown:false,
    };

    constructor(props){
        super(props)
        this.state={
          user: "",
          refreshing: false,
          Matchs: [],
        }
    }

    AllMatch = () => {
      // console.log("salut c'est moi", this.props.navigation.state.params.id)

        fetch(annexe.ip+"match/all_match")
        .then(res => res.json())
        .then(res => {
            this.setState({Matchs: res.data})
        }).catch((error) => console.error("Erreur AllMatch: " ,error));
    }

    _onRefresh = () => {
        this.setState({refreshing: true});
        this.fetchData().then(() => {
            this.setState({refreshing: false});
          });
    }

    fetchData = async() => {
        this.getPublicGame()
    }

    getPublicGame() {
        const header = {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
        };
        fetch(annexe.ip+"match/all_match", header)
        .then(res => res.json())
        .then(res => {console.log(res.public_games)
        this.setState({data_public: res.public_games})
    })
        .catch(error => console.error("Erreur PublicGame: ", error))
    }

    _recupUser = async () => {
        try {
            const value = await AsyncStorage.getItem('user');
            if (value !== null) {
                this.setState({user: JSON.parse(value)})
                console.log("User: ",this.state.user.token);

            }
        } catch (error) {
            console.error("Erreur User: ",error)
        }
    };

    componentDidMount = async () => {
        this.AllMatch()
    }

  render() {
    return (
    //<ImageBackground source={require('../../assets/StatFiveV3.png')} style={{width: '100%', height: '100%', opacity: 0.95}}>
        <KeyboardAvoidingView style={style.containerView} behavior="padding">
            <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
                <View style={style.header}>
                    <Text style={style.logoText}>
                        <Text style={{color:'white'}}>Accueil </Text>
                    </Text>
                    <Icon style={style.icon_trophy} name="trophy" size={36} onPress={() => this.props.navigation.navigate("LeaderBoard", {id: this.props.navigation.state.params.id})}></Icon>
                    <Icon style={style.icon_profil} name="user" size={36} onPress={() => this.props.navigation.navigate("Profil", {id: this.props.navigation.state.params.id})}></Icon>
                </View>
            </TouchableWithoutFeedback>
            <View>
                <ScrollView
                        refreshControl={
                            <RefreshControl
                                refreshing={this.state.refreshing}
                                onRefresh={this._onRefresh.bind(this)}
                            />} >
                    <List>
                        <ListItem>
                            <Text style={style.FirstLetter}>Historique de Matchs</Text>
                        </ListItem>
                        { this.state.Matchs.map(data => ( <ListItem >
                            <TouchableOpacity key={data.id} onPress={() =>  this.props.navigation.navigate('StatGame', {id: data.id})} title="0">
                                <Text  style={style.listItems}>{data.name} | ID : {data.id}</Text>
                            </TouchableOpacity>
                        </ListItem>
                        ) ) }
                    </List>
                </ScrollView>
            </View>
        </KeyboardAvoidingView>
    //</ImageBackground>
    );
  }
}
