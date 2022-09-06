import { Flex, useColorModeValue, Box, Input, Heading, Button, Stack, Link, Image, Alert, AlertDescription, CloseButton, AlertIcon, Center } from '@chakra-ui/react'
import { useState } from 'react';
import { useRouter } from 'next/router'
import { API_URL } from "../static";
import { register } from "@mokhta_s/react-statfive-api"

export default function Inscription() {
  const [email, setEmail] = useState("");
  const [pass, setPass] = useState("");
  const [pass2, setPass2] = useState("");
  const [firstname, setFirstname] = useState("");
  const [lastname, setLastname] = useState("");
  const [error, setError] = useState(null)

  const bg = useColorModeValue("blueteal.500", "blueteal.500")
  const router = useRouter()

  const reg = async () => {
    if(pass !== pass2)
      return setError("Les mots de passe ne correspondent pas")
    if(lastname.length < 2 || firstname < 2) 
      return setError("Le prénom ou le nom est trop court")
    if(!isEmail(email)) {
      let result = await register(API_URL, email, firstname, lastname, pass, pass2)
      if(!(result?.data?.error))
        router.push('/')
      else
      setError(result.data.message)
    } else {
      return setError("L'email n'est pas conforme.")
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
      <Box >
      <Flex boxShadow="2xl" w="400px" h="auto" bgColor="white" borderRadius="15px" justifyContent="center" p="20px" flexDir="column">
        <Image alt="Logo de StatFive" src="statfive.png" w="175px" m="auto"/>
        {error && 
        <Alert status="error" borderRadius="10px" mb="10px">
          <AlertIcon />
          <AlertDescription mr={2}>{error}</AlertDescription>
          <CloseButton position="absolute" right="8px" top="8px" />
        </Alert>
        }
        <Heading textAlign="center" mb="30px">Inscription</Heading>
        <Flex flexDir="column" w="100%">
          <Input placeholder="Nom" mb="15px" value={lastname} onChange={(e) => setLastname(e.target.value)}/>
          <Input placeholder="Prénom" mb="15px" value={firstname} onChange={(e) => setFirstname(e.target.value)} />
          <Input placeholder="E-mail" mb="15px" borderColor={isEmail(email) ? "crimson" : "green.200"} value={email} onChange={(e) => setEmail(e.target.value)}/>
          <Input placeholder="Mot de passe" type="password" mb="15px" value={pass} onChange={(e) => setPass(e.target.value)}/>
          <Input placeholder="Confirmer le mot de passe" type="password" mb="30px" value={pass2} onChange={(e) => setPass2(e.target.value)} />
        </Flex>
        <Stack direction="row" spacing={4}>
            <Button colorScheme="blue" href="/accueil" onClick={reg}>Valider</Button>
            <Link href="/">
                <Button colorScheme="blue" variant="outline">Déjà inscrit ?</Button>
            </Link>
        </Stack>
      </Flex>
    </Box>  
    </Center>
    
  )
}
