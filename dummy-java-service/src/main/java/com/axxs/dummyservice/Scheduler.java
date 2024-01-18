package com.axxs.dummyservice;

import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.Scheduled;

@Configuration
@EnableScheduling
@Slf4j
public class Scheduler {

    @Scheduled(fixedRate = 1000)
    public void scheduleFixedRateTask() {


        log.info("This is a info log");
        log.debug("This is a debug log");
        log.error("This is a error log");
    }
}
