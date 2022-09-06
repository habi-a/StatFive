import { useColorModeValue, PinInput, PinInputField, HStack,  Alert, AlertDescription, AlertIcon, Flex, Heading, AlertTitle, Center } from '@chakra-ui/react'
import { useEffect, useState } from 'react';
import { API_URL } from "../static";
import { useRouter } from 'next/router'
import {useStore} from "./index"
import Router from 'next/router'
import { verification } from '@mokhta_s/react-statfive-api'


const Verification = () => {
    const [error, setError] = useState(null)
    const token = useStore(state => state.token)
    const setCheck = useStore(state => state.setCheck)
    const data = useStore(state => state.data)
    const setData = useStore(state => state.addData)
    const addVerif = useStore(state => state.addVerif)
    const router = useRouter()

    const verif = async (value) => {
        if(value.length < 1) {
            setError("Aucun champ n'a été rempli")
            return;
        }
        const result = await verification(value);
        console.log(result)
        if(result && !(result?.data?.error)) {
            setData(result.data)
            addVerif(true)
            router.push('accueil')
            setCheck()
        } else {
            setError(result.data.message)
        }
    }

    useEffect(() => {
        if(data && data.verification === true) {
            Router.replace('/accueil')
        }
    }, [data])

    return (
    <Center w="100%" h="100vh"
        bgColor="blueteal.500">
        <Flex
        p={8}
        rounded="lg"
        boxShadow="black"
        zIndex={100}
        flexDir="column"
        alignItems="center"
        border="1px solid white"
      >
        <Heading size="md" fontWeight="600" mb={5} color="white">Veuillez saisir le code reçu sur votre boîte mail</Heading>
        <HStack>
          <PinInput
            onComplete={verif}
            autoFocus
            isInvalid={error ? true : false}
            type='alphanumeric'
          >
            <PinInputField bgColor="blueteal.500" color="white" />
            <PinInputField bgColor="blueteal.500" color="white" />
            <PinInputField bgColor="blueteal.500" color="white" />
            <PinInputField bgColor="blueteal.500" color="white" />
            <PinInputField bgColor="blueteal.500" color="white" />
            <PinInputField bgColor="blueteal.500" color="white" />
          </PinInput>
        </HStack>
        {error && (
          <Alert status="error" mt={5} roundedRight="md" variant="left-accent">
            <AlertIcon />
            <AlertTitle>Erreur : </AlertTitle>
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}
      </Flex>  
      </Center>
    )
}

export default Verification