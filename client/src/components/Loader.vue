<template>
    <div class="h-full flex flex-col justify-center items-center">
        <div class="flex flex-col justify-center items-center gap-6">
            <span class="loader"></span>
            <div class="text-2xl font-medium text-gray-700" id="loader-message">{{ activ }}</div>
        </div>
    </div>
</template>

<script>
export default {
  name: 'Loader',
  props: {
    messages: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      activ: '',
      currentMessageIndex: 0,
      currentCharIndex: 0
    };
  },
  mounted() {
    setTimeout(this.displayMessages(), 1000);
  },
  methods: {
    displayTextOneCharacterAtATime(text, delay, callback) {
        const displayDiv = document.getElementById("loader-message");
        let index = 0;
        displayDiv.textContent = ''; // Clear previous text

        // Function to add one character at a time
        function addCharacter() {
            if (index < text.length) {
                displayDiv.textContent += text[index];
                index++;
                setTimeout(addCharacter, delay);
            } else if (callback) {
                callback();
            }
        }
        addCharacter();
    },
    displayMessages() {
        let messageIndex = 0;
        const displayNextMessage = () => {
            if (messageIndex < this.messages.length) {
                this.displayTextOneCharacterAtATime(this.messages[messageIndex], 100, () => {
                    messageIndex++;
                    setTimeout(displayNextMessage, 500); // Pause for 2 seconds before displaying the next message
                });
            } else {
                // Restart the loop
                messageIndex = 0;
                setTimeout(displayNextMessage, 500); // Pause for 2 seconds before restarting the loop
            }
        };
        displayNextMessage();
    }
  }
}
</script>

<style scoped>
.loader {
  width: 60px;
  height: 60px;
  border: 8px solid #000;
  border-radius: 50%;
  display: inline-block;
  box-sizing: border-box;
  position: relative;
  animation: pulse 1s linear infinite;
}
.loader:after {
  content: '';
  position: absolute;
  width: 60px;
  height: 60px;
  border: 8px solid #000;
  border-radius: 50%;
  display: inline-block;
  box-sizing: border-box;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  animation: scaleUp 1s linear infinite;
}

@keyframes scaleUp {
  0% { transform: translate(-50%, -50%) scale(0) }
  60% , 100% { transform: translate(-50%, -50%)  scale(1)}
}
@keyframes pulse {
  0% , 60% , 100%{ transform:  scale(1) }
  80% { transform:  scale(1.2)}
}

</style>