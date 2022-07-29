import { extendTheme } from '@chakra-ui/react'

const config = {
    initialColorMode: "light",
}

const theme = extendTheme({
  colors: {
    blueteal: {
      500: "#0190F8"
    },
  },
  styles: {
      global: {
          li: {
            width: '100%'
          },
      },
  },
  config
})

export default theme