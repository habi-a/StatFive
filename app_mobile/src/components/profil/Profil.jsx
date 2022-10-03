import React, { useState, useEffect } from 'react';
import {
  Text,
        View,
        Alert, Image} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useNavigation } from '@react-navigation/core';
import { getUserInfo, getMe } from '@mokhta_s/react-statfive-api';
import style from "./index";
import Icon from 'react-native-vector-icons/FontAwesome';
import { AnimatedCircularProgress } from 'react-native-circular-progress';


const ProfilScreen = () => {
    const [user, setUser] = useState({})
    const [stats, setStats] = useState(null);
    const [complex, setComplex] = useState(null);
    const [allComplex, setAllComplex] = useState(null);
    const navigation = useNavigation();

    useEffect(() => {
      getMeInfo()
    }, [])

    const getMeInfo = async () => {
      const result = await getMe();
      console.log('ici', result.data.data)
      if (!result.data.error) {
        if (result.data.data.complexes) {
          setAllComplex(result.data.data.complexes);
        } else {
          setStats(result.data.data.stats);
          setComplex(result.data.data.complex);
          setUser(result.data.data);
        }
    }
    }

  const onLogout = () => {
      Alert.alert(
          'Attention',
          'Voulez-vous vraiment être déconnecter ?',
          [
            {text: 'Oui, je souhaite me déconnecter', onPress: () => clearAsyncStorage()},
            {
              text: 'Non',
              onPress: () => console.log('Cancel Pressed'),
              style: 'cancel',
            },
          ],
          {cancelable: false},
        );
  }

  const clearAsyncStorage = async () => {
    await AsyncStorage.clear();
    navigation.navigate("Login");
  }

    return (
        <View style={style.container}>
          <View style={style.header}>
              <Icon style={style.icon_home} name="home" size={36} onPress={() => navigation.navigate('Accueil')}></Icon>
              <Icon style={style.icon_logout} name="sign-out" size={36} onPress={() => onLogout()}></Icon>
          </View>
          <Image
            style={style.avatar}
            source={require('../../../public/StatFiveV3.png')}
          />
          <View style={style.body}>
            <View style={style.bodyContent}>
              <Text style={style.name}>{user?.firstname} {user?.lastname}</Text>
              <Text style={style.info}>Super-Admin</Text>
              <Text style={style.description}>{user?.description}</Text>
              <Text style={style.email}>{user?.email}</Text>
            </View>
            <View>
              <Text style={style.email}>
                Statistiques des équipes de
              </Text>
              <Text style={style.infoUser}>
                {user?.lastname} {user?.firstname}
              </Text>
              <View style={style.stats}>
               <AnimatedCircularProgress
                size={120}
                width={10}
                fill={100}
                tintColor="#00e0ff"
                backgroundColor="#3d5875">
                   {
                      (fill) => (
                        <Text>
                          {stats?.nb_but} {stats ? "but" : ""}
                          {stats?.nb_but > 0 ? "s" : ""}
                        </Text>
                      )
                    }
                </AnimatedCircularProgress>
                <AnimatedCircularProgress
                size={120}
                width={10}
                fill={100}
                tintColor="#00e0ff"
                backgroundColor="#3d5875">
                   {
                      (fill) => (
                        <Text>
                          {stats?.nb_match} {stats ? "match" : ""}
                          {stats?.nb_match > 0 ? "s" : ""}
                        </Text>
                      )
                    }
                </AnimatedCircularProgress> 
              </View>
              
            </View>
          </View>
        </View>
    );
}

export default ProfilScreen;