import React, { Component } from 'react';
import { createStackNavigator } from 'react-navigation-stack';
import { createAppContainer } from 'react-navigation';
import {Text,
        View,
        RefreshControl,
        Alert,
        Image,
        TouchableOpacity,
        AsyncStorage} from 'react-native';
import { ScrollView } from "react-native-gesture-handler";
import Icon from 'react-native-vector-icons/FontAwesome';
import { LineChart } from "react-native-chart-kit";
import { Dimensions } from 'react-native';

import style from "./style";
import annexe from '../../api_link'

const line = {
      labels: ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N'],
      datasets: [
        {
          data: [
            Math.random() * 100,
            Math.random() * 100,
            Math.random() * 100,
            Math.random() * 100,
            Math.random() * 100,
            Math.random() * 100,
            Math.random() * 100,
            Math.random() * 100,
            Math.random() * 100,
            Math.random() * 100,
            Math.random() * 100,
          ],
          strokeWidth: 2, // optional
        },
      ],
    };

const chartConfig = {
  backgroundColor: 'white',
  backgroundGradientFrom: '#0090F8',
  backgroundGradientTo: '#696969',
  decimalPlaces: 2, // optional, defaults to 2dp
  color: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
  style: {
    borderRadius: 16
  }
};

export default class ProfilScreen extends Component {

  static navigationOptions = {
      headerShown:false,
    };

    constructor(props){
          super(props)
          this.state={
            refreshing: false,
            user: {}
      }
  }

  Profil = () => {
      fetch(annexe.ip+"users/"+this.props.navigation.state.params.id)
      .then(res => res.json())
      .then(res => {
        console.log(res)
          this.setState({user: res.data})
      }).catch((error) => console.error("Erreur Profil: " ,error));
  }

  _onRefresh = () => {
      this.setState({refreshing: true});
      this.fetchData().then(() => {
          this.setState({refreshing: false});
        });
  }

  onLogout() {
      Alert.alert(
          'Attention',
          'Voulez-vous vraiment quitter l\'application ?',
          [
            {text: 'Oui, je le souhaite', onPress: () => this.clearAsyncStorage()},
            {
              text: 'Non',
              onPress: () => console.log('Cancel Pressed'),
              style: 'cancel',
            },
          ],
          {cancelable: false},
        );
  }

  clearAsyncStorage = async() => {
    AsyncStorage.clear();
    this.props.navigation.navigate("Login");
  }

  componentDidMount = async () => {
      this.Profil()
  }

  render() {
    return (
      <ScrollView
          refreshControl={
              <RefreshControl
                  refreshing={this.state.refreshing}
                  onRefresh={this._onRefresh.bind(this)}
      />} >
        <View style={style.container}>
          <View style={style.header}>
              <Icon style={style.icon_home} name="home" size={36} onPress={() => this.props.navigation.navigate("Home")}></Icon>
              <Icon style={style.icon_logout} name="sign-out" size={36} onPress={() => this.onLogout()}></Icon>
          </View>
          <Image
            style={style.avatar}
            source={require('../../assets/StatFiveV3.png')}
          />
          <View style={style.body}>
            <View style={style.bodyContent}>
              <Text style={style.name}>{this.state.user.firstname} {this.state.user.lastname}</Text>
              <Text style={style.info}>Super-Admin</Text>
              <Text style={style.description}>{this.state.user.description}</Text>
              <Text style={style.email}>{this.state.user.email}</Text>
              <View style={{flexDirection: 'row', justifyContent:'space-around', marginTop: 30}}>
                <Text style={style.titre}>Match(s) Analysé(s) :   </Text>
                <Text style={style.nbr_matchs}>11</Text>
              </View>
            </View>
          </View>
            <View>
              <LineChart
                data={line}
                width={Dimensions.get('window').width-10} // from react-native
                height={200}
                yAxisLabel={''}
                chartConfig={chartConfig}
                bezier
                style={{
                  marginLeft: 10,
                  marginRight: 10,
                  borderRadius: 16
                }}
              />
            </View>
        </View>
      </ScrollView>
    );
  }
}
