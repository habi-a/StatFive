import { Flex, Text, Box, Heading, List, ListItem, ListIcon, Link } from '@chakra-ui/react'
import styles from '../styles/Home.module.css'
import SimpleSidebar from "../components/Menu"
import Anchor from "../components/Anchor"
import { Line, Doughnut } from 'react-chartjs-2';
import { data, options, dataPass, dataVictory } from '../static/data';
import { GiTrophyCup, GiMedal } from "react-icons/gi"

export default function Accueil() {

  return (
    <Box>
        <SimpleSidebar />
        <Box pos="relative" left="240px" w="calc(100% -  240px)">
            <Heading textAlign="center">Accueil</Heading>
            <Flex w="700px" h="auto" mb="75px" ml="125px">
                <Line data={data} options={options} />
                <Line data={dataPass} options={options} />
            </Flex>
            <Flex flexDir="row" justifyContent="space-around">
                <Box ml="125px">
                    <Heading mb="25px" >Classement général</Heading>
                    <Flex justifyContent="center" w="100%">
                        <List spacing={3} textAlign="center" w="100%">
                            <ListItem bgColor="#84C9D5" cursor="pointer"> <ListIcon as={GiTrophyCup} color="gold" />Utilisateur 1</ListItem>
                            <ListItem bgColor="#C1E4EA" cursor="pointer"> <ListIcon as={GiMedal} color="silver" />Utilisateur 2</ListItem>
                            <ListItem bgColor="#E6F4F7" cursor="pointer"> <ListIcon as={GiMedal} color="bronze" />Utilisateur 3</ListItem>
                            <ListItem bgColor="#F3FAFB" cursor="pointer"> Utilisateur 4</ListItem>
                            <ListItem bgColor="#F3FAFB" cursor="pointer" mb="10px"> Utilisateur 5</ListItem>
                            <Link href="/classement" color="blueteal.500">
                                <Text>Voir plus..</Text>
                            </Link>
                        </List>
                    </Flex>
                </Box>
                <Box  w="300px" h="300px">
                    <Doughnut data={dataVictory} />
                </Box>
            </Flex>
        </Box>
    </Box>
  )
}
