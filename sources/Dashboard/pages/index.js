import { Flex, Text, useColorModeValue, Box, Input, Heading, Button, Stack, Link, Image, Alert, AlertDescription, CloseButton, AlertIcon } from '@chakra-ui/react'
import { useState } from 'react';
import styles from '../styles/Home.module.css'
import axios from "axios"
import { API_URL } from "../static";
import { useRouter } from 'next/router'
import create from 'zustand'
import { persist } from "zustand/middleware"
import PasswordStrengthBar from 'react-password-strength-bar';

export const useStore = create(persist((set) => ({
  token: null,
  verification: false,
  userValue: null,
  addToken: (tok) => set(() => ({ token: tok })),
  addVerif: (ver) => set(() => ({ verification: ver })),
  addValue: (i) => set(() => ({ userValue: i }))
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
  
  const token = useStore(state => state.token)
  const login = async () => {
    if(!isEmail(email) )
      await axios.post(
          [API_URL] + "/users/login",
          {
              email,
              password: pass
            }
        ).then(res => {
          addToken(res.data.data.token);
          addVerif(res.data.data.verification);
          addValue(res.data.data.id)
          if(res.data.data.verification) 
            router.push("/accueil"); 
          else
            router.push("/verification")})
        .catch(err => {
          setError(err && err.response && err.response.data.message)
        });
}

  const isEmail = (val) => {
    let regEmail = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    if(!regEmail.test(val)){
      return true;
    }
  }

  return (
    <Box bgColor={bg} className={styles.container}>
      <Flex boxShadow="2xl" w="400px" h="auto" bgColor="white" borderRadius="15px" justifyContent="center" p="20px" flexDir="column">
        <Image src="statfive.png" w="175px" m="auto"/>
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
            <Button colorScheme="blue" href="/accueil" onClick={() => login()}>Se connecter</Button>
          <Link href="/inscription">
            <Button colorScheme="blue" variant="outline">S'inscrire</Button>
          </Link>
        </Stack>
      </Flex>
    </Box>
  )
}