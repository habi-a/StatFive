import { Flex, Box, Heading, List, ListItem, ListIcon, Button, Text, AspectRatio } from '@chakra-ui/react'
import SimpleSidebar from "../components/Menu"
import { GiSoccerField } from "react-icons/gi"
import Modal from 'react-modal';
import { useEffect, useState } from 'react';
import axios from "axios"
import { API_URL } from "../static";
import withAuth from '../components/withAuth';


const customStyles = {
  content: {
    top: '50%',
    left: '50%',
    right: 'auto',
    bottom: 'auto',
    marginRight: '-50%',
    transform: 'translate(-50%, -50%)',
  },
};

const Historique = () => {
  const [modalIsOpen, setIsOpen] = useState(false);
  const [matchList, setMatchList] = useState([]);
  const [matchData, setMatchData] = useState(null)
  const [teamOne, setTeamOne] = useState(null)
  const [teamTwo, setTeamTwo] = useState(null)

  useEffect(() => {
    matchListHistoric()
  }, [])

  const matchListHistoric = async () => {
    await axios.get(
        API_URL + `/match/all_match`).then(res => setMatchList(res.data.data))
      .catch(err => {
        console.log(err)
      });
  }

  const openModal = async (id) => {
    const dataMatch = await axios.get(API_URL + `/match/stat_match_by_id/${id}`)
    setMatchData(dataMatch.data.data)
    const getInfoTeamOne = axios.get(API_URL + `/team/${dataMatch.data.data.stats[0].team_id}`)
    const getInfoTeamTwo = axios.get(API_URL + `/team/${dataMatch.data.data.stats[1].team_id}`)
    axios.all([getInfoTeamOne, getInfoTeamTwo]).then(axios.spread((...responses) => {
      setTeamOne(responses[0].data.data)
      setTeamTwo(responses[1].data.data)
    })).catch(errors => {
      console.log(errors)
    })
    setIsOpen(true);
  }

  function closeModal() {
    setIsOpen(false);
  }

  return (
    <Box>
        <SimpleSidebar />
        <Box pos="relative" left="240px" w="calc(100% -  240px)">
            <Heading textAlign="center" mb="50px">Historique des matchs</Heading>
            <Flex justifyContent="center" w="100%">
              <List spacing={3} textAlign="center" w="100%">
                {matchList.map((elm) => {
                  return <ListItem bgColor="#84C9D5" cursor="pointer" p="10px" w="100%" onClick={() => openModal(elm.id)}> <ListIcon as={GiSoccerField} color="green" />ID DU MATCH : {elm.id} | Match {elm.name}</ListItem>
                })}
              </List>
            </Flex>
        </Box>
        <Modal
              isOpen={modalIsOpen}
              onRequestClose={closeModal}
              style={customStyles}
              contentLabel="Example Modal"
            >
              <Heading textAlign="center" mb="25px">Match</Heading>
              <Flex w="300px" h="auto" justifyContent="space-around">
                <Box>
                  <Text>Equipe {teamOne && teamOne.team.name}<br/><br/></Text>
                  <hr/>
                  <Text>But : {matchData && matchData.stats[0].goals}<br/><br/></Text>
                  <hr/>
                  <Text>Possession : {matchData && matchData.stats[0].possesion}<br/><br/></Text>
                </Box>
                <Box>
                  <Text>Equipe {teamTwo && teamTwo.team.name}<br/><br/></Text>
                  <hr/>
                  <Text>But : {matchData && matchData.stats[1].goals}<br/><br/></Text>
                  <hr/>
                  <Text>Possession : {matchData && matchData.stats[1].possesion}<br/><br/></Text>
                </Box>
                
                
              </Flex>
              <Text>Vidéo du match : </Text>
              <AspectRatio maxW="560px" ratio={1}>
                  <iframe
                    title="naruto"
                    src={matchData && matchData.path}
                    allowFullScreen
                  />
                </AspectRatio>
              <Button onClick={closeModal} mt="25px">Fermer</Button>
            </Modal>
    </Box>
  )
}

export default withAuth(Historique)
