# Use Node.js image
FROM node:20 


# Set working directory
WORKDIR /

# Copy package files and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy all other project files
COPY . .

# Expose the default Next.js port
EXPOSE 3000

# Start the Next.js development server
CMD ["npm", "run", "dev"]
