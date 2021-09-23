import { Flex, Text, useColorModeValue, Box, Input, Heading, Button, Stack, Link, Image, Alert, AlertDescription, CloseButton, AlertIcon } from '@chakra-ui/react'
import styles from '../styles/Home.module.css'
import { useState } from 'react';
import { useRouter } from 'next/router'
import axios from "axios"
import { API_URL } from "../static";

import PasswordStrengthBar from 'react-password-strength-bar';

export default function Inscription() {
  const [email, setEmail] = useState("");
  const [pass, setPass] = useState("");
  const [pass2, setPass2] = useState("");
  const [firstname, setFirstname] = useState("");
  const [lastname, setLastname] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null)
  const [strength, setStrength] = useState(null);

  const bg = useColorModeValue("blueteal.500", "blueteal.500")
  const router = useRouter()

  const register = async () => {
    if(pass !== pass2)
      return setError("Les mots de passe ne correspondent pas")
    if(lastname.length < 2 || firstname < 2) 
      return setError("Le prénom ou le nom est trop court")
    if(!isEmail(email))
      await axios.post(
          [API_URL] + "/users/create",
          {
              email,
              firstname,
              lastname,
              password: pass
            }
        ).then(res => router.push("/"))
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
        <Heading textAlign="center" mb="30px">Inscription</Heading>
        <Flex flexDir="column" w="100%">
          <Input placeholder="Nom" mb="15px" value={lastname} onChange={(e) => setLastname(e.target.value)}/>
          <Input placeholder="Prénom" mb="15px" value={firstname} onChange={(e) => setFirstname(e.target.value)} />
          <Input placeholder="E-mail" mb="15px" borderColor={isEmail(email) ? "crimson" : "green.200"} value={email} onChange={(e) => setEmail(e.target.value)}/>
          <Input placeholder="Mot de passe" type="password" mb="15px" value={pass} onChange={(e) => setPass(e.target.value)}/>
          <PasswordStrengthBar password={pass} scoreWords={["simple", "simple", "ok", "bon", "très bon"]} shortScoreWord="trop court" onChangeScore={(val) => setStrength(val)}/>
          <Input placeholder="Confirmer le mot de passe" type="password" mb="30px" value={pass2} onChange={(e) => setPass2(e.target.value)} />
        </Flex>
        <Stack direction="row" spacing={4}>
            <Button colorScheme="blue" href="/accueil" onClick={register}>Valider</Button>
            <Link href="/">
                <Button colorScheme="blue" variant="outline">Déjà inscrit ?</Button>
            </Link>
        </Stack>
      </Flex>
    </Box>
  )
}
