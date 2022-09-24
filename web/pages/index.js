import { Flex, useColorModeValue, Box, Input, Heading, Button, Stack, Link, Image, Alert, AlertDescription, CloseButton, AlertIcon, Center, Divider } from '@chakra-ui/react'
import { useState } from 'react';
import styles from '../styles/Home.module.css'
import { API_URL } from "../static";
import { useRouter } from 'next/router'
import create from 'zustand'
import { persist } from "zustand/middleware"
import { login } from "@mokhta_s/react-statfive-api"

export const useStore = create(persist((set) => ({
  token: null,
  verification: false,
  userValue: null,
  data: null,
  teamUser: [],
  check: false,
  addToken: (tok) => set(() => ({ token: tok })),
  addVerif: (ver) => set(() => ({ verification: ver })),
  addValue: (i) => set(() => ({ userValue: i })),
  addData: (data) => set(() => ({ data: data })),
  addTeam: (team) => set((state) => ({ teamUser: [...state.teamUser, team]})),
  resetTeam: (team) => set(() => ({ teamUser: []})),
  resetID: (id) => set((state) => ({teamUser: state.teamUser.filter((todo) => todo !== id)})),
  setCheck: () => set(() => ({ check: true })),
  deleteEverything: () => set({ }, true),
})))

export default function Home() {
  const [email, setEmail] = useState("");
  const [pass, setPass] = useState("");
  const [error, setError] = useState(null)

  const bg = useColorModeValue("blueteal.500", "blueteal.500")
  const router = useRouter()
  const addToken = useStore(state => state.addToken)
  const addVerif = useStore(state => state.addVerif)
  const addValue = useStore(state => state.addValue)
  const addData = useStore(state => state.addData)
  const setCheck = useStore(state => state.setCheck)

   const log = async () => {
      const res = await login(API_URL, email, pass)
      if(res === "L'email n'est pas conforme.") {
        setError(res)
        return;
      }
      if(res.data.error) {
        setError(res.data.message)
      } else {
        addToken(res.data.token);
        addVerif(res.data.verification);
        addValue(res.data.id)
        addData(res.data)
        if(res.data.verification) {
          router.push("/accueil"); 
          setCheck()
        } else {
          router.push("/verification")
        }
      }
 }

  const isEmail = (val) => {
    let regEmail = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    if(!regEmail.test(val)){
      return true;
    }
  }

  return (
    <Center bgColor={bg} h="100vh">
      <Box>
        <Flex boxShadow="2xl" w="400px" h="auto" bgColor="white" borderRadius="15px" justifyContent="center" p="20px" flexDir="column">
          <Image alt="Logo de StatFive" src="statfive.png" w="175px" m="auto"/>
          {error && 
          <Alert status="error" borderRadius="10px" mb="10px">
            <AlertIcon />
            <AlertDescription mr={2}>{error}</AlertDescription>
            <CloseButton position="absolute" right="8px" top="8px" />
          </Alert>
          }
          <Heading textAlign="center" mb="30px">Connexion</Heading>
          <Flex flexDir="column" w="100%">
            <Input placeholder="E-mail" mb="15px" borderColor={isEmail(email) ? "crimson" : "green.200"} value={email} onChange={(e) => setEmail(e.target.value)}/>
            <Input placeholder="Mot de passe" type="password" mb="30px" value={pass} onChange={(e) => setPass(e.target.value)}/>
          </Flex>
          <Stack direction="row" spacing={4}>
              <Button colorScheme="blue" href="/accueil" onClick={() => log()}>Se connecter</Button>
            <Link href="/inscription">
              <Button colorScheme="blue" variant="outline">Inscription</Button>
            </Link>
          </Stack>
              <Link mt="15px" colorScheme="white" color="black" href="/reset-password">Mot de passe oublié ?</Link>
        </Flex>
      </Box>
    </Center>
  )
}
