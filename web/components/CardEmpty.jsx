import {
    Heading,
    Box,
    Center,
    Flex,
    Button,
    useColorModeValue,
    Modal,
    ModalOverlay,
    ModalContent,
    ModalHeader,
    ModalFooter,
    ModalBody,
    ModalCloseButton
  } from '@chakra-ui/react';
import { useState } from 'react';
import axios from "axios"
import { API_URL } from "../static";
import Card  from './Card'
import {useStore} from "../pages/index"
import { getAllUser } from "@mokhta_s/react-statfive-api"

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
  
  export default function CardEmpty() {
  const [modalIsOpen, setIsOpen] = useState(false);
  const [userList, setUserList] = useState([]);
  const [player, setPlayer] = useState(false);
  const [playerInfo, setPlayerInfo] = useState(null)

  const addTeam = useStore(state => state.addTeam)


  const userListMatch = async () => {
    const result = await getAllUser();
    if(!result?.data.error) {
      setUserList(result.data.data)
    }
  }

    function openModal() {
      userListMatch()
      setIsOpen(true);
    }
  
    function closeModal() {
      setIsOpen(false);
    }

    return (
      !player ? 
      <Center py={6}>
        <Flex
          maxW={'270px'}
            justifyContent="center"
            alignItems="center"
          w={'full'}
          bg={useColorModeValue('white', 'gray.800')}
          boxShadow={'2xl'}
          rounded={'md'}
          overflow={'hidden'}
            h="360px">
              <Button
              onClick={openModal}
            bg={useColorModeValue('#151f21', 'gray.900')}
            color={'white'}
            rounded={'md'}
            _hover={{
              transform: 'translateY(-2px)',
              boxShadow: 'lg',
            }}>
            Ajouter un joueur à l'équipe
          </Button>

        <Modal isOpen={modalIsOpen} onClose={closeModal}>
          <ModalOverlay />
          <ModalContent>
            <ModalHeader>Statistique du match</ModalHeader>
            <ModalCloseButton />
            <ModalBody>
              <Heading>Liste des joueurs</Heading>
                  {
                    userList.map((elm) => {
                      return <Box mb="10px" mt="10px" p="10px" cursor="pointer">{elm.firstname} | {elm.lastname} <Button position="absolute" right="25px" colorScheme="teal" size="xs" onClick={() => {setPlayer(!player); setPlayerInfo(elm); addTeam(elm.id)}}>Ajouter</Button><hr/></Box>
                    })
                  }
            </ModalBody>

            <ModalFooter>
              <Button colorScheme='blue' mr={3} onClick={closeModal}>
                Fermer
              </Button>
            </ModalFooter>
          </ModalContent>
        </Modal>
      </Flex>
      </Center>
          : <Card info={playerInfo} delUser={setPlayer}/>  
    );
  }