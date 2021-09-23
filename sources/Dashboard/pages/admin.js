import { Flex, Text, Box, Heading, List, ListItem, ListIcon, Link, Select, Button } from '@chakra-ui/react'
import styles from '../styles/Home.module.css'
import SimpleSidebar from "../components/Menu"
import Anchor from "../components/Anchor"
import { Line, Doughnut } from 'react-chartjs-2';
import { data, options, dataPass, dataVictory } from '../static/data';
import { GiTrophyCup, GiMedal } from "react-icons/gi"
import { useEffect } from 'react';
import { useRouter } from 'next/router'
import {useStore} from "./index"
import FileInput from '@brainhubeu/react-file-input';

export default function Admin() {
    const idUser = useStore(state => state.userValue)
    const router = useRouter()

    useEffect(() => {
        if(idUser !== 3) {
            router.push('/accueil')
        }
    }, [])

  return (
    <Box>
        <SimpleSidebar />
        <Box pos="relative" left="240px" w="calc(100% -  240px)">
                    <Heading textAlign="center" mb="25px">Création du match</Heading>
                    <Flex>
                    <Select placeholder="Choisissez une équipe">
                        <option value="option1">jaouad</option>
                        <option value="option2">red</option>
                        <option value="option3">blue</option>
                        <option value="option3">green</option>
                        <option value="option3">yellow</option>
                        <option value="option3">violet</option>
                        </Select>
                    <Select placeholder="Choisissez une équipe">
                        <option value="option1">jaouad</option>
                        <option value="option2">red</option>
                        <option value="option3">blue</option>
                        <option value="option3">green</option>
                        <option value="option3">yellow</option>
                        <option value="option3">violet</option>
                    </Select>
                    </Flex>
                    <Flex justifyContent="center" alignItems="center" flexDirection="column" mt="25px">
                        <FileInput
                        label='Ajouter la vidéo du match'
                        />
                    <Button mt="25px">Valider la création</Button>
                    </Flex>
        </Box>
    </Box>
  )
}
