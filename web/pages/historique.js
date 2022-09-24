import { Flex, Box, Heading,Text, AspectRatio,
  Center,
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionIcon,
  AccordionPanel,
  Select } from '@chakra-ui/react'
import SimpleSidebar from "../components/Menu"
import { useEffect, useState } from 'react';
import withAuth from '../components/withAuth';
import { matchListHistoric, statMatchById } from "@mokhta_s/react-statfive-api"
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';
import { API_URL } from '../static';

const Historique = () => {
  const [matchList, setMatchList] = useState([]);
  const [matchData, setMatchData] = useState(null);
  const [allComplexe, setAllComplexe] = useState([]);

  useEffect(() => {
    async function getM() {
      const user = await AsyncStorage.getItem('userInfo');
      const userInfo = JSON.parse(user);
      if(userInfo && userInfo.role < 2) {
        getMatch()
      } else {
        getAllComplexe()
      }
    }
    getM()
  }, [])

  const getMatch = async (idComplex) => {
    const token = await AsyncStorage.getItem('token');
    const user = await AsyncStorage.getItem('userInfo');
    const userInfo = JSON.parse(user);
    if(userInfo && userInfo.role < 2 ) {
      const result = await axios.get(API_URL + `/match/get-my-match`,  { headers:{"api-token": token} })
      if(!result.data?.error) {
        setMatchList(result.data.data)
      }
    } else {
      const resultat = await axios.get(API_URL + "/match/get-match-by-complex/" + idComplex, { headers: {"api-token": token}})
      if(!resultat.data?.error) {
        setMatchList(resultat.data.data)
      }
    }

  }

  const getAllComplexe = async () => {
    const token = await AsyncStorage.getItem('token');
    const user = await AsyncStorage.getItem('userInfo');
    const userInfo = JSON.parse(user);
    if(userInfo && userInfo.role === 2) {
      const result = await axios.get(API_URL + `/admin/list-complex`, { headers:{"api-token": token} })
          if(!result?.data.error) {
              setAllComplexe(result.data.data)
          }
    }
  }

  const openModal = async (id) => {
    const result = await statMatchById(id)
    setMatchData(result.data.data)
  }

  return (
    <Box>
        <SimpleSidebar />
        <Box pos="relative" left={{sm: "100px", md: "240px"}} w={{ md:"calc(100% -  240px)"}}>
            <Heading textAlign="center" mb="50px">Historique des matchs</Heading>
            {allComplexe?.length > 0 &&<Select w="25%" m="5px auto" placeholder="Choisir un complexe" onChange={(e) => e.target.value && getMatch(e.target.value) }>
                                    {allComplexe && allComplexe.length > 0 &&
                                    allComplexe.map((el, i) => 
                                        <option key={i} value={`${el.id}`}>{el.name}</option>
                                    )
                                }
              </Select>}
              {matchList && matchList.length <  1 && <Heading mt="25px" w="100%" size="md" textAlign="center">Aucune information n'a été trouvé</Heading>}
              <Center>
                <Accordion w="100%" mt="25px" allowToggle>
                  {matchList.map((elm, i) => {
                    return <AccordionItem>
                    <h2>
                      <AccordionButton onClick={() => {elm.finish && openModal(elm.id)}} _expanded={{ bg: '#002B5B', color: 'white' }}>
                        <Box flex='1' textAlign='left'>
                        {!elm.finish && "ANALYSE EN COURS - "} Match n° {elm.id} | Match {elm.name}
                        </Box>
                        <AccordionIcon />
                      </AccordionButton>
                    </h2>
                    <AccordionPanel padding="inherit">
                    <Flex h="auto">
                <Box w="50%">
                  <Text p="5" fontSize="26px" fontWeight="700" backgroundColor="#3DB2FF" color="white" textAlign="center" borderRight="1px solid #002B5B" borderBottom="1px solid #002B5B">{matchData && matchData.team_blue.name}</Text>
                  <Text p="3" fontSize="18px" fontWeight="500" backgroundColor="#F9F5EB" color="#3DB2FF" textAlign="center" borderRight="1px solid #002B5B" borderBottom="2px solid #002B5B">But : {matchData && matchData.team_blue.goals}</Text>
                  <Text p="3" fontSize="18px" fontWeight="500" backgroundColor="#F9F5EB" color="#3DB2FF" textAlign="center" borderRight="1px solid #002B5B" borderBottom="2px solid #002B5B">Possession : {matchData && Math.round(matchData.team_blue.possesion)} %</Text>
                </Box>
                <Box w="50%">
                  <Text p="5" fontSize="26px" fontWeight="700" backgroundColor="#3DB2FF" color="white" textAlign="center" borderLeft="1px solid #002B5B" borderBottom="1px solid #002B5B">{matchData && matchData.team_red.name}</Text>
                  <Text p="3" fontSize="18px" fontWeight="500" backgroundColor="#F9F5EB" color="#3DB2FF" textAlign="center" borderLeft="1px solid #002B5B" borderBottom="2px solid #002B5B">But : {matchData && matchData.team_red.goals}</Text>
                  <Text p="3" fontSize="18px" fontWeight="500" backgroundColor="#F9F5EB" color="#3DB2FF" textAlign="center" borderLeft="1px solid #002B5B" borderBottom="2px solid #002B5B">Possession : {matchData && Math.round(matchData.team_red.possesion)} %</Text>
                </Box>
              </Flex>
              <Text textAlign="center" fontWeight="700" fontSize="26px">Vidéo du match</Text>
              <AspectRatio w="480px" h="270px" ratio={1} m="5px auto">
                  <iframe
                    title="video_match"
                    src={matchData && matchData.path}
                    allowFullScreen
                  />
                </AspectRatio>
                    </AccordionPanel>
                  </AccordionItem>
                  })}
                </Accordion>
              </Center>
        </Box>
    </Box>
  )
}

export default withAuth(Historique)
