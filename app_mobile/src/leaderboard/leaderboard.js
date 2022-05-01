import React, { Component } from 'react';
import { createStackNavigator } from 'react-navigation-stack';
import { createAppContainer } from 'react-navigation';
import {Text,
        View,
        Image,
        TouchableOpacity} from 'react-native';
import { ScrollView } from "react-native-gesture-handler";
import Icon from 'react-native-vector-icons/FontAwesome';
import LeaderBoard from 'react-native-leaderboard';
import { Dimensions } from 'react-native';
import { SafeAreaView } from 'react-navigation';

import style from "./style";
import annexe from '../../api_link'

export default class LeaderBoardScreen extends Component {

  static navigationOptions = {
      headerShown:false,
    };

    constructor(props){
      super(props)
      this.state = {
          data: [
              {userName: 'Joe', highScore: 52},
              {userName: 'Jenny', highScore: 120},
              {userName: 'Franck.C', highScore: 420},
              {userName: 'Brandon', highScore: 322},
              {userName: 'Acal', highScore: 260},
              {userName: 'Barbara', highScore: 11},
              {userName: 'Bernard', highScore: 86},
              {userName: 'LockLear', highScore: 76},
              {userName: 'Doigby', highScore: 0},
              {userName: 'Mcfly', highScore: 35},
              {userName: 'Carlito', highScore: 60},
              {userName: 'Noob', highScore: 0},
              {userName: 'Joe', highScore: 52},
              {userName: 'Jenny', highScore: 120},
              {userName: 'Franck', highScore: 420},
              {userName: 'Brandon', highScore: 322},
              {userName: 'Acal', highScore: 260},
              {userName: 'Barbara', highScore: 11},
              {userName: 'Bernard', highScore: 86},
              {userName: 'LockLear', highScore: 76},
              {userName: 'Doigby', highScore: 0},
              {userName: 'Mcfly', highScore: 35},
              {userName: 'Carlito', highScore: 60},
              {userName: 'Noob', highScore: 0},
              //...
          ], //can also be an object of objects!: data: {a:{}, b:{}}
          user: {},
      }
    }

    LeaderBoard = () => {
        fetch(annexe.ip+"users/"+this.props.navigation.state.params.id)
        .then(res => res.json())
        .then(res => {
          console.log(res)
            this.setState({user: res.data})
        }).catch((error) => console.error("Erreur LeaderBoard: " ,error));
    }

    componentDidMount = async () => {
        this.LeaderBoard()
    }

  render() {
    return (
      <View style={style.container}>
        <View style={style.header}>
          <Icon style={style.icon_home} name="home" size={36} onPress={() => this.props.navigation.navigate("Home")}></Icon>
          <Text style={style.name_board}>{this.state.user.firstname}.{this.state.user.lastname}</Text>
          <Text style={style.position}>Top : 1</Text>
        </View>
        <Image
          style={style.avatar}
          source={require('../../assets/StatFiveV3.png')}
        />
        <SafeAreaView style={{marginTop: 70,height:Dimensions.get('window').height-220}}>
          <View style={style.bodyContent}>
            <LeaderBoard
              data={this.state.data}
              sortBy='highScore'
              labelBy='userName'
              containerStyle={{width:Dimensions.get('window').width-10}}
              rankStyle={style.rankStyle}
              labelStyle={style.labelStyle}
              scoreStyle={style.scoreStyle}
              oddRowColor='#479AD3'
              evenRowColor='#0090F8'/>
          </View>
        </SafeAreaView>
      </View>
    );
  }
}
