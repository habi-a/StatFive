import { Flex, Box, Heading, List, ListItem, ListIcon, Button, Text, AspectRatio, Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton, } from '@chakra-ui/react'
import SimpleSidebar from "../components/Menu"
import { GiSoccerField } from "react-icons/gi"
import { useEffect, useState } from 'react';
import axios from "axios"
import { API_URL } from "../static";
import withAuth from '../components/withAuth';
import { matchListHistoric, statMatchById } from "@mokhta_s/react-statfive-api"

const Historique = () => {
  const [modalIsOpen, setIsOpen] = useState(false);
  const [matchList, setMatchList] = useState([]);
  const [matchData, setMatchData] = useState(null)

  useEffect(() => {
    matchHistoric()
  }, [])

  const matchHistoric = async () => {
    let result = await matchListHistoric()
    setMatchList(result)
  }

  const openModal = async (id) => {
    const result = await statMatchById(id)
    console.log(result)
    setMatchData(result.data.data)
    setIsOpen(true);
  }

  function closeModal() {
    setIsOpen(false);
  }

  return (
    <Box>
        <SimpleSidebar />
        <Box pos="relative" left={{sm: "100px", md: "240px"}} w={{ md:"calc(100% -  240px)"}}>
            <Heading textAlign="center" mb="50px">Historique des matchs</Heading>
            <Flex justifyContent="center" w="100%">
              <List spacing={3} textAlign="center" w="100%">
                {matchList.map((elm, i) => {
                  return <ListItem key={i} bgColor="#84C9D5" cursor={elm.finish ? "pointer" : "not-allowed"} p="10px" w="100%" onClick={() => {elm.finish && openModal(elm.id)}}> <ListIcon as={GiSoccerField} color="green" />{!elm.finish && "ANALYSE EN COURS"} - ID DU MATCH : {elm.id} | Match {elm.name}</ListItem>
                })}
              </List>
            </Flex>
        </Box>
        <Modal isOpen={modalIsOpen} onClose={closeModal}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Statistique du match</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
          <Heading textAlign="center" mb="25px">Match</Heading>
              <Flex w="300px" h="auto" justifyContent="space-around">
                <Box>
                  <Text>Equipe {matchData && matchData.team_blue.name}<br/><br/></Text>
                  <hr/>
                  <Text>But : {matchData && matchData.team_blue.goals}<br/><br/></Text>
                  <hr/>
                  <Text>Possession : {matchData && matchData.team_blue.possesion}<br/><br/></Text>
                </Box>
                <Box>
                  <Text>Equipe {matchData && matchData.team_red.name}<br/><br/></Text>
                  <hr/>
                  <Text>But : {matchData && matchData.team_red.goals}<br/><br/></Text>
                  <hr/>
                  <Text>Possession : {matchData && matchData.team_red.possesion}<br/><br/></Text>
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
          </ModalBody>

          <ModalFooter>
            <Button colorScheme='blue' mr={3} onClick={closeModal}>
              Fermer
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </Box>
  )
}

export default withAuth(Historique)
