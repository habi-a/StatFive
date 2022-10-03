import {
    Heading,
    Box,
    Center,
    Flex,
    Button,
    Modal,
    ModalOverlay,
    ModalContent,
    ModalHeader,
    ModalFooter,
    ModalBody,
    ModalCloseButton
  } from '@chakra-ui/react';
import { useState } from 'react';
import Card  from './Card'
import {useStore} from "../pages/index"
import { getAllUser } from "@mokhta_s/react-statfive-api"
  
  export default function CardEmpty({numberID}) {
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
          w='full'
          bg="white"
          boxShadow='2xl'
          rounded='md'
          overflow='hidden'
          h="360px">
              <Button
              datatestid={`equipe_new_player-${numberID}`}
              onClick={openModal}
              bg="#151f21"
              color='white'
              rounded='md'
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
                    userList.map((elm, i) => {
                      return <Box key={i} mb="10px" mt="10px" p="10px" cursor="pointer">{elm.firstname} | {elm.lastname} <Button datatestid={`new_player_${i}`} position="absolute" right="25px" colorScheme="teal" size="xs" onClick={() => {setPlayer(!player); setPlayerInfo(elm); addTeam(elm.id)}}>Ajouter</Button><hr/></Box>
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