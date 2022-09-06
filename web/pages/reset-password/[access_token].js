import { Flex, useColorModeValue, Box, Input, Heading, Button, Stack, Link, Image, Alert, AlertDescription, CloseButton, AlertIcon, Center, Divider } from '@chakra-ui/react'
import { useState } from 'react';
import { useRouter } from 'next/router'
import create from 'zustand'
import { persist } from "zustand/middleware"
import { changeMyPassword } from "@mokhta_s/react-statfive-api"

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
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null)

  const bg = useColorModeValue("blueteal.500", "blueteal.500")
  const router = useRouter()

   const changePassword = async () => {
      const res = await changeMyPassword(router.query.access_token, password)
      if(!(res?.data?.error)) {
        router.push('/')
      } else {
        setError(res.data.message)
      }
 }

  return (
    <Center bgColor={bg} h="100vh">
      <Box>
        <Flex boxShadow="2xl" w="400px" h="auto" bgColor="white" borderRadius="15px" justifyContent="center" p="20px" flexDir="column">
          <Image alt="Logo de StatFive" src="../statfive.png" w="175px" m="auto"/>
          {error && 
          <Alert status="error" borderRadius="10px" mb="10px">
            <AlertIcon />
            <AlertDescription mr={2}>{error}</AlertDescription>
            <CloseButton position="absolute" right="8px" top="8px" />
          </Alert>
          }
          <Heading textAlign="center" mb="30px">Nouveau mot de passe</Heading>
          <Flex flexDir="column" w="100%">
            <Input placeholder="Nouveau mot de passe" mb="15px" value={password} onChange={(e) => setPassword(e.target.value)}/>
          </Flex>
          <Stack direction="row" spacing={4}>
              <Button colorScheme="blue" href="/accueil" onClick={() => changePassword()}>Valider</Button>
            <Link href="/">
              <Button colorScheme="blue" variant="outline">Retour</Button>
            </Link>
          </Stack>
        </Flex>
      </Box>
    </Center>
  )
}
