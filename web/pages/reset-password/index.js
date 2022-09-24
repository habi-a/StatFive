import { Flex, useColorModeValue, Box, Input, Heading, Button, Stack, Link, Image, Alert, AlertDescription, CloseButton, AlertIcon, Center, Text } from '@chakra-ui/react'
import { useState } from 'react';
import { getNewPassword } from "@mokhta_s/react-statfive-api"

export default function Home() {
  const [email, setEmail] = useState("");
  const [error, setError] = useState(null)
  const [validation ,setValidation] = useState(false)

  const bg = useColorModeValue("blueteal.500", "blueteal.500")

   const sendMailPassword = async () => {
      const res = await getNewPassword(email)
      if(!(res?.data?.error)) {
        setValidation(true)
      } else {
        setError(res.data.message)
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
        {!validation ? <Flex boxShadow="2xl" w="400px" h="auto" bgColor="white" borderRadius="15px" justifyContent="center" p="20px" flexDir="column">
          <Image alt="Logo de StatFive" src="statfive.png" w="175px" m="auto"/>
          {error && 
          <Alert status="error" borderRadius="10px" mb="10px">
            <AlertIcon />
            <AlertDescription mr={2}>{error}</AlertDescription>
            <CloseButton position="absolute" right="8px" top="8px" />
          </Alert>
          }
          <Heading textAlign="center" mb="30px">Récupérer son compte</Heading>
          <Flex flexDir="column" w="100%">
            <Input placeholder="E-mail" mb="15px" borderColor={isEmail(email) ? "crimson" : "green.200"} value={email} onChange={(e) => setEmail(e.target.value)}/>
          </Flex>
          <Stack direction="row" spacing={4}>
              <Button colorScheme="blue" href="/accueil" onClick={() => sendMailPassword()}>Valider</Button>
            <Link href="/">
              <Button colorScheme="blue" variant="outline">Retour</Button>
            </Link>
          </Stack>
        </Flex> : 
        <Flex boxShadow="2xl" w="400px" h="auto" bgColor="white" borderRadius="15px" justifyContent="center" p="20px" flexDir="column">
        <Image alt="Logo de StatFive" src="statfive.png" w="175px" m="auto"/>

        <Heading textAlign="center" mb="30px">Votre boîte mail</Heading>
        <Flex flexDir="column" w="100%" textAlign="center">
          <Text mb="15px">Un lien pour réinitialiser votre mot de passe a été envoyé sur la boîte mail avec laquelle vous vous êtes inscrit</Text>
        </Flex>
        <Stack direction="row" spacing={4}>
          <Link href="/">
            <Button colorScheme="blue" variant="outline">Page de connexion</Button>
          </Link>
        </Stack>
      </Flex>
      }
      </Box>
    </Center>
  )
}
