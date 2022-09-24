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
          body: {
            background: "#F9F5EB",
          },
          li: {
            width: '100%'
          },
          h2: {
            color: "#1C3879",
          }
      },
  },
  config
})

export default theme