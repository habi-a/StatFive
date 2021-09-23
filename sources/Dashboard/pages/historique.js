import { Flex, Box, Heading, List, ListItem, ListIcon, Button, Text } from '@chakra-ui/react'
import SimpleSidebar from "../components/Menu"
import { GiTrophyCup, GiMedal, GiSoccerField } from "react-icons/gi"
import Modal from 'react-modal';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/router'
import axios from "axios"
import { API_URL } from "../static";



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

export default function Historique() {
  const [modalIsOpen, setIsOpen] = useState(false);
  const [matchList, setMatchList] = useState([]);
  const [matchData, setMatchData] = useState(null)

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
    await axios.get(
      API_URL + `/match/stat_match_by_id/${id}`).then(res => setMatchData(res.data.data))
    .catch(err => {
      console.log(err)
    });
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
              <Heading>Match</Heading>
              <Flex w="300px" h="300px" justifyContent="space-around">
                <Box>
                  <Text>Equipe {matchData && matchData.stats[0].color}<br/><br/></Text>
                  <hr/>
                  <Text>But : {matchData && matchData.stats[0].goals}<br/><br/></Text>
                  <hr/>
                  <Text>Possession : {matchData && matchData.stats[0].possesion}<br/><br/></Text>
                </Box>
                <Box>
                  <Text>Equipe {matchData && matchData.stats[1].color}<br/><br/></Text>
                  <hr/>
                  <Text>But : {matchData && matchData.stats[1].goals}<br/><br/></Text>
                  <hr/>
                  <Text>Possession : {matchData && matchData.stats[1].possesion}<br/><br/></Text>
                </Box>
              </Flex>
              {console.log(matchData)}
              <Button onClick={closeModal} mt="25px">Fermer</Button>
            </Modal>
    </Box>
  )
}
