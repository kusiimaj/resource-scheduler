#  Node.js image as a build stage
FROM node:18 AS build

# working directory inside the container
WORKDIR /app

#  3: Copy package.json and package-lock.json first
COPY package.json package-lock.json ./

#  4: Install dependencies
RUN npm install

#  5: Copy the rest of the application files
COPY . .

#  6: Build the React app
RUN npm run build

#  7: Use Nginx to serve the frontend
FROM nginx:alpine

#  8: Copy the built frontend files to Nginx's default HTML directory
COPY --from=build /app/build /usr/share/nginx/html

#  9: Expose port 80
EXPOSE 80

#  10: Start Nginx when the container runs
CMD ["nginx", "-g", "daemon off;"]
