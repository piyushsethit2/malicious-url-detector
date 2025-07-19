# Enhanced Content Analysis System

## 🚀 **Overview**

The Enhanced Content Analysis System is a powerful, multi-strategy approach to analyzing website content for malicious indicators, regardless of whether the site is accessible or not. This system provides comprehensive coverage and improved accuracy for URL threat detection.

## 🎯 **Key Features**

### **1. Multi-Strategy Content Fetching**
The system uses 5 different strategies to attempt content retrieval:

#### **Strategy 1: Direct HTTP Request**
```java
// Standard HTTP request with common User-Agent
HttpRequest request = HttpRequest.newBuilder()
    .uri(uri)
    .header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    .timeout(Duration.ofSeconds(10))
    .build();
```

#### **Strategy 2: Custom User-Agent**
```java
// Alternative User-Agent for sites that block standard browsers
.header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
.header("Accept-Encoding", "gzip, deflate, br")
.header("DNT", "1")
```

#### **Strategy 3: HTTP Fallback**
```java
// Try HTTP if HTTPS fails
if (url.startsWith("https://")) {
    String httpUrl = url.replace("https://", "http://");
    result = fetchContentDirect(httpUrl);
}
```

#### **Strategy 4: WWW Prefix Removal**
```java
// Try without www prefix
if (url.contains("www.")) {
    String noWwwUrl = url.replace("www.", "");
    result = fetchContentDirect(noWwwUrl);
}
```

#### **Strategy 5: WWW Prefix Addition**
```java
// Try with www prefix
if (!url.contains("www.") && url.contains("://")) {
    String withWwwUrl = url.replace("://", "://www.");
    result = fetchContentDirect(withWwwUrl);
}
```

### **2. URL Structure Analysis**
Even when content is inaccessible, the system analyzes URL structure:

#### **Suspicious URL Shortening Services**
```java
Pattern SUSPICIOUS_DOMAINS = Pattern.compile(
    "(?i)(bit\\.ly|goo\\.gl|tinyurl|is\\.gd|t\\.co|fb\\.me|ow\\.ly|su\\.pr|twurl|snipurl|short\\.to|BudURL|ping\\.fm|tr\\.im|zip\\.net|sn\\.im|short\\.ie|kl\\.am|wp\\.me|rubyurl|om\\.ly|to\\.ly|bit\\.do|t\\.co|lnkd\\.in|db\\.tt|qr\\.ae|adf\\.ly|goo\\.gl|bitly\\.com|cur\\.lv|tiny\\.cc|ow\\.ly|bit\\.ly|adcrun\\.ch|ity\\.im|q\\.gs|is\\.gd|po\\.st|bc\\.vc|twitthis\\.com|u\\.to|j\\.mp|buzurl\\.com|cutt\\.us|u\\.bb|yourls\\.org|x\\.co|prettylinkpro\\.com|scrnch\\.me|filoops\\.info|vzturl\\.com|qr\\.net|1url\\.com|tweez\\.me|v\\.gd|tr\\.im|link\\.zip\\.net)"
);
```

#### **Malicious File Extensions**
```java
Pattern MALICIOUS_EXTENSIONS = Pattern.compile(
    "(?i)\\.(exe|bat|cmd|com|pif|scr|vbs|js|jar|msi|dmg|app|deb|rpm|apk|ipa|pl|py|sh|ps1|psm1|vbe|wsf|hta|chm|reg|inf|lnk|url|scf|wsh|wsc|msc|gadget|application|appref-ms|appx|appxbundle|msix|msixbundle|msu|msp|mst|ocx|dll|sys|drv|bin|dat|tmp|temp|cache|log|bak|old|swp|swo|lock|pid|sock|fifo|pipe|socket|device|proc|sys|dev|etc|var|usr|home|root|boot|mnt|media|opt|srv|sbin|lib|lib64|bin|sbin|usr|local|share|doc|man|info|include|src|build|dist|target|out|bin|obj|debug|release|build|dist|target|out|bin|obj|debug|release)$"
);
```

#### **Suspicious IP Patterns**
```java
Pattern SUSPICIOUS_IP_PATTERNS = Pattern.compile(
    "(?i)(10\\.|172\\.(1[6-9]|2[0-9]|3[01])\\.|192\\.168\\.|127\\.|0\\.|169\\.254\\.|224\\.|240\\.)"
);
```

### **3. Domain Reputation Analysis**
```java
private double analyzeDomainReputation(String url, List<String> issues) {
    // Check for unusually long domain names
    if (domain.length() > 50) {
        issues.add("Unusually long domain name");
        confidence += 0.2;
    }
    
    // Check for random-looking domains
    if (isRandomLookingDomain(domain)) {
        issues.add("Random-looking domain name");
        confidence += 0.3;
    }
}
```

### **4. Network Indicators**
```java
private double analyzeNetworkIndicators(String url, List<String> issues) {
    // Check if domain resolves
    InetAddress address = InetAddress.getByName(domain);
    
    // Check for private IP addresses
    if (address.isSiteLocalAddress() || address.isLoopbackAddress()) {
        issues.add("Private/local IP address detected");
        confidence += 0.4;
    }
    
    // Check for suspicious IP ranges
    String ip = address.getHostAddress();
    if (ip.startsWith("10.") || ip.startsWith("172.") || ip.startsWith("192.168.")) {
        issues.add("Private network IP detected");
        confidence += 0.3;
    }
}
```

## 🔍 **Content Analysis Capabilities**

### **1. JavaScript Analysis**
```java
Pattern SUSPICIOUS_JS_PATTERNS = Pattern.compile(
    "(?i)(eval\\s*\\(|Function\\s*\\(|unescape|fromCharCode|String\\.fromCharCode|document\\.write\\s*\\(|innerHTML\\s*=|setTimeout\\s*\\(|setInterval\\s*\\()"
);
```

**Detects:**
- `eval()` function calls
- Dynamic function creation
- String manipulation for obfuscation
- DOM manipulation
- Timer-based execution

### **2. Phishing Form Detection**
```java
Pattern PHISHING_FORM_PATTERNS = Pattern.compile(
    "(?i)(<form[^>]*>.*?(password|login|username|email|credit.?card|social.?security|ssn|bank|account|verify|pin|security|authentication)[^>]*>)"
);
```

**Detects:**
- Login forms
- Password fields
- Credit card forms
- Social security number fields
- Bank account forms
- Authentication forms

### **3. Suspicious iframe Detection**
```java
Pattern SUSPICIOUS_IFRAME_PATTERNS = Pattern.compile(
    "(?i)(<iframe[^>]*src=[\"']([^\"']*)[\"'][^>]*>)"
);
```

**Detects:**
- Hidden iframes
- Cross-origin iframes
- Suspicious iframe sources

### **4. Redirect Analysis**
```java
Pattern REDIRECT_PATTERNS = Pattern.compile(
    "(?i)(window\\.location|location\\.href|document\\.location|meta.*?refresh|http-equiv.*?refresh|window\\.open|document\\.domain)"
);
```

**Detects:**
- JavaScript redirects
- Meta refresh redirects
- Window opening
- Document domain manipulation

### **5. Obfuscated Content Detection**
```java
Pattern OBFUSCATED_CONTENT_PATTERNS = Pattern.compile(
    "(?i)(base64|%[0-9a-fA-F]{2}|&#x[0-9a-fA-F]+|\\\\x[0-9a-fA-F]{2}|\\u[0-9a-fA-F]{4}|\\x[0-9a-fA-F]{2})"
);
```

**Detects:**
- Base64 encoding
- URL encoding
- HTML entity encoding
- Unicode encoding
- Hex encoding

### **6. Suspicious Keywords**
```java
Pattern SUSPICIOUS_KEYWORDS = Pattern.compile(
    "(?i)(malware|virus|trojan|spyware|phishing|scam|fake|hack|crack|warez|keygen|nulled|premium|cheat|bot|exploit|vulnerability|backdoor|rootkit|keylogger|ransomware|adware|spam|download|free|cracked|hack|cheat|bot|exploit|bypass|inject|sql|xss|csrf|ddos|brute|force|overflow|buffer|shell|reverse|bind|meterpreter|payload|dropper|loader|stager|beacon|c2|command|control)"
);
```

**Detects:**
- Malware-related terms
- Hacking tools
- Exploit references
- Security bypass terms
- Command and control terms

## 📊 **Analysis Results**

### **Content Analysis Result Structure**
```java
private static class ContentAnalysisResult {
    String content;        // The actual HTML content (if accessible)
    boolean accessible;    // Whether the site was accessible
    String error;         // Error message if failed
}
```

### **Detection Confidence Scoring**
- **URL Structure Analysis**: 0.2-0.4 confidence
- **Domain Reputation**: 0.2-0.3 confidence
- **Network Indicators**: 0.2-0.4 confidence
- **JavaScript Analysis**: 0.3 confidence
- **Phishing Forms**: 0.4 confidence
- **Suspicious iframes**: 0.3 confidence
- **Redirects**: 0.25 confidence
- **Obfuscated Content**: 0.35 confidence
- **Suspicious Keywords**: 0.2 confidence
- **External Resources**: 0.3 confidence
- **Suspicious Links**: 0.25 confidence
- **Meta Tags**: 0.3 confidence
- **Script Sources**: 0.3 confidence

## 🎯 **Use Cases**

### **1. Accessible Sites**
- Full content analysis
- JavaScript evaluation
- Form detection
- Resource analysis
- Link analysis

### **2. Inaccessible Sites**
- URL structure analysis
- Domain reputation checking
- Network indicator analysis
- IP address validation
- Domain resolution checking

### **3. Partially Accessible Sites**
- Fallback strategy execution
- Partial content analysis
- Error pattern recognition
- Accessibility as threat indicator

## 🔧 **Integration**

### **Spring Boot Integration**
```java
@Service
public class EnhancedContentAnalyzerService implements BaseDetectionService {
    // Automatically integrated into the detection pipeline
}
```

### **Detection Pipeline**
```java
// Enhanced content analysis (always enabled for better coverage)
CompletableFuture<UrlScanResult.DetectionResult> enhancedContentFuture = 
    CompletableFuture.supplyAsync(() -> {
        try {
            return enhancedContentAnalyzer.detect(normalizedUrl);
        } catch (Exception e) {
            return new UrlScanResult.DetectionResult(
                "Enhanced Content Analysis", false, "Error: " + e.getMessage(), 0.0
            );
        }
    }, executorService);
futures.add(enhancedContentFuture);
```

## 📈 **Performance Benefits**

### **1. Improved Coverage**
- **Before**: Only analyzed accessible sites
- **After**: Analyzes all sites regardless of accessibility

### **2. Better Accuracy**
- **Before**: Single strategy content fetching
- **After**: 5-strategy fallback approach

### **3. Enhanced Detection**
- **Before**: Basic content patterns
- **After**: Comprehensive pattern library

### **4. Reduced False Negatives**
- **Before**: Missed inaccessible malicious sites
- **After**: Detects threats even when content is unavailable

## 🚀 **Example Usage**

### **Accessible Site Analysis**
```
URL: https://malicious-site.com/phishing
Result: 
- Content: <form action="steal.php"><input type="password">
- JavaScript: eval(String.fromCharCode(...))
- Confidence: 0.85
- Issues: ["Potential phishing form detected", "Suspicious JavaScript detected"]
```

### **Inaccessible Site Analysis**
```
URL: https://suspicious-domain-12345.com
Result:
- Content: null (inaccessible)
- Domain: Random-looking domain name
- Network: Domain does not resolve
- Confidence: 0.4
- Issues: ["Random-looking domain name", "Domain does not resolve"]
```

## 🎉 **Benefits**

1. **Universal Coverage**: Analyzes sites whether accessible or not
2. **Multi-Strategy Approach**: 5 different content fetching strategies
3. **Comprehensive Detection**: 13 different analysis categories
4. **High Accuracy**: Detailed pattern matching and heuristics
5. **Performance Optimized**: Fast analysis with reasonable timeouts
6. **Error Resilient**: Graceful handling of network issues
7. **Extensible**: Easy to add new patterns and strategies

This enhanced system provides significantly better coverage and accuracy for URL threat detection, especially for sites that are intentionally made inaccessible or use anti-detection techniques. 