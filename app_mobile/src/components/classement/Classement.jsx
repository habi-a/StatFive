import React, { useEffect, useState } from 'react';
import {Text,
        View,
        Image,
    FlatList} from 'react-native';
import Icon from 'react-native-vector-icons/FontAwesome';
import LeaderBoard from 'react-native-leaderboard';
import AsyncStorage from '@react-native-async-storage/async-storage';

import style from "./index";
import { useNavigation } from '@react-navigation/native';
import { getAverageGoal } from '@mokhta_s/react-statfive-api';

const ClassementScreen = () => {
    const [data, setData] = useState([])
    const [firstname, setFirstname] = useState('')
    const [lastname, setLastname] = useState('')
    const [refreshing, setRefreshing] = useState(false)
    const navigation = useNavigation()

       useEffect(() => {
        async function fetchData() {
            try {
                const value = await AsyncStorage.getItem('userInfo')
                if(value !== null) {
                  setFirstname(JSON.parse(value).firstname)
                  setLastname(JSON.parse(value).lastname)
                }
            } catch(e) {
                console.log("error", e)
            }
        }
        fetchData();
        getLeaderboard()
    }, [])


    const getLeaderboard = async () => {
        const result = await getAverageGoal()
        console.log('result', result)
        if(result && result.length > 0) {
            setData(result)
        }
    }    


    return (
      <View style={style.container}>
        <View style={style.header}>
          <Icon style={style.icon_home} name="home" size={36} onPress={() => navigation.navigate('Accueil')}></Icon>
          <Text style={style.name_board}>{firstname} {lastname}</Text>
        </View>
        <Image
          style={style.avatar}
          source={require('../../../public/StatFiveV3.png')}
        />
          <View style={style.bodyContent}>
                    <LeaderBoard
                    data={data}
                    sortBy='moyenne_goal'
                    labelBy='name'
                    rankStyle={style.rankStyle}
                    labelStyle={style.labelStyle}
                    scoreStyle={style.scoreStyle}
                    oddRowColor='#479AD3'
                    evenRowColor='#0090F8'/>
          </View>
      </View>
    );
}

export default ClassementScreen