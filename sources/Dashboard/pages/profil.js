import { Flex, Text, Box, Heading, List, ListItem, ListIcon, Link } from '@chakra-ui/react'
import styles from '../styles/Home.module.css'
import SimpleSidebar from "../components/Menu"
import Card from "../components/Card"
import CardEmpty from '../components/CardEmpty'

export default function Profil() {
  return (
    <Box>
        <SimpleSidebar />
        <Box pos="relative" left="240px" w="calc(100% -  240px)">
            <Heading textAlign="center">Mon profil</Heading>
            <Flex flexDir="row" justifyContent="space-between" padding="40px">
                <Card />
                <CardEmpty />
                <CardEmpty />
                <CardEmpty />
                <CardEmpty />
            </Flex>
        </Box>
    </Box>
  )
}
