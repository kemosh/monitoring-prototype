package com.axxs.dummyservice;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class WebController {

	@GetMapping("/different-endpoint")
	public String index() {
		return "Greetings from Spring Boot!";
	}

}
