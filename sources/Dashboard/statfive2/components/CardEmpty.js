import {
    Heading,
    Avatar,
    Box,
    Center,
    Image,
    Flex,
    Text,
    Stack,
    Button,
    useColorModeValue,
  } from '@chakra-ui/react';
import Modal from 'react-modal';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/router'
import axios from "axios"
import { API_URL } from "../static";
import Card  from './Card'
import {useStore} from "../pages/index"

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
  const checkArray = useStore(state => state.teamUser)
  const resetTeam = useStore(state => state.resetTeam)


  const userListMatch = async () => {
    await axios.get(
        API_URL + `/users/all_user`).then(res => setUserList(res.data.data))
      .catch(err => {
        console.log(err)
      });
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
            w='270px'
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

          <Modal
              isOpen={modalIsOpen}
              onRequestClose={closeModal}
              style={customStyles}
              contentLabel="Example Modal"
            >
              <Heading>Liste des joueurs</Heading>
              {
                userList.map((elm) => {
                  return <Box mb="10px" mt="10px" p="10px" cursor="pointer">{elm.firstname} | {elm.lastname} <Button position="absolute" right="25px" colorScheme="teal" size="xs" onClick={() => {setPlayer(!player); setPlayerInfo(elm); addTeam(elm.id)}}>Ajouter</Button><hr/></Box>
                })
              }
              <Button onClick={closeModal} mt="25px">Fermer</Button>
            </Modal>
        </Flex>
      </Center>
          : <Card info={playerInfo} delUser={setPlayer}/>  
    );
  }