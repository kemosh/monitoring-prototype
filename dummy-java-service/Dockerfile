FROM eclipse-temurin:17-jdk AS builder

WORKDIR /build

COPY . /build

RUN chmod +x gradlew
RUN ./gradlew build --no-daemon

FROM eclipse-temurin:17-jre

RUN mkdir /app

# Create user with predefined uid to avoid problems with mounting logs dir
RUN addgroup --gid 2000 spring && adduser --uid 2000 --ingroup spring spring
RUN chown spring:spring /app
USER spring:spring

COPY --from=builder /build/build/libs/dummy-service-0.1.jar /app/spring-boot-application.jar

ENTRYPOINT ["java", "-XX:+UnlockExperimentalVMOptions", "-Djava.security.egd=file:/dev/./urandom","-jar","/app/spring-boot-application.jar"]

