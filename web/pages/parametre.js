import { Flex, Text, Box, Heading, Textarea, IconButton, useColorMode, Button, Select, Link, Image } from '@chakra-ui/react'
import SimpleSidebar from "../components/Menu"
import { MoonIcon, SunIcon } from "@chakra-ui/icons";
import {useStore} from "./index"
import { useState } from 'react';
import axios from "axios"
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { API_URL } from "../static";
import withAuth from '../components/withAuth';

const Parametre = () => {
    const { colorMode, toggleColorMode } = useColorMode();
    const idUser = useStore(state => state.userValue)
    const dataUser = useStore(state => state.data)
    const logOut = useStore(state => state.deleteEverything)
    const [description, setDescription] = useState(dataUser ? dataUser.description : '');
    const [poste, setPoste] = useState(dataUser ? dataUser.post : '' )

    const updateProfil = async () => {
          await axios.put(
              [API_URL] + `/users/${idUser}`,
              { description, post: poste})
            .then(res => {
                toast.success('Le profil a bien été modifié', {
                    position: "bottom-right",
                    autoClose: 5000,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true,
                    progress: undefined,
                    });
                console.log('Profil bien modifié')
            })
            .catch(err => console.log('Erreur', err)
            );
    }

  return (
    <Box>
        <SimpleSidebar />
        <Box pos="relative" left="240px" w="calc(100% -  240px)">
            <Heading textAlign="center" mb="50px">Mes paramètres</Heading>
            <Flex flexDir="column" >
                <Flex mb="25px" justifyContent="center">
                <Text>Changer de mode : </Text>
                    <IconButton
                    ml="10px"
                    size="sm"
                    w="auto !important"
                    onClick={toggleColorMode}
                    icon={colorMode === "dark" ? <SunIcon /> : <MoonIcon />}
                    id="toggleColorMode"
                    as="div"
                    role="button"
                    />
                </Flex>
                <Flex justifyContent="center">
                    <Flex flexDir="column" mb="25px" >
                        <Heading>Modifier mes informations :</Heading>
                        <Textarea placeholder="Ajouter une description" value={description && description.length > 0 ? description : ""} onChange={(e) => setDescription(e.target.value)} mt="25px"/>
                        <Select placeholder="Choisissez votre poste" value={poste && poste.length > 0 ? poste : ""} onChange={(e) => setPoste(e.target.value)} mt="25px">
                            <option value="Attaquant">Attaquant</option>
                            <option value="Défenseur">Défenseur</option>
                            <option value="Gardien">Gardien</option>
                        </Select>
                        <Button onClick={() => updateProfil()} mt="25px">Enregistrer mes modifications</Button>
                        <ToastContainer
                            position="bottom-right"
                            autoClose={5000}
                            hideProgressBar={false}
                            newestOnTop={false}
                            closeOnClick
                            rtl={false}
                            pauseOnFocusLoss
                            draggable
                            pauseOnHover
                        />
                    </Flex>
                </Flex>
                <Flex flexDirection="column" ml="40px" alignItems="center">
                    <Text as="h1" fontWeight="bold">Application pour mobile :</Text>
                    <Flex alignItems="center" >
                        <Text>Vous pouvez scanner le qr code ci-dessous ou bien vous dirigez sur ce <Link isExternal color="blue.500" href="exp://exp.host/@fr4nck/StatFiveV3">lien</Link> depuis un mobile </Text>
                        <Image  ml="10px" boxSize="150px" src="qr-code.png"/>
                    </Flex>
                    
                </Flex>
                <Flex mt="50px">
                    <Link m="auto" href="/"><Button onClick={() => logOut()} color="white" background="black">Se déconnecter</Button></Link>
                    <Button m="auto" w="25%" colorScheme="red" isDisabled>Supprimer mon compte</Button>
                </Flex>
            </Flex>
        </Box>
    </Box>
  )
}

export default withAuth(Parametre)